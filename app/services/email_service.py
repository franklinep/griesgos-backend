# app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from smtplib import SMTPException, SMTPConnectError

load_dotenv()

class EmailService:
    _otp_store: Dict[str, dict] = {}  # {email: {otp, expiration}}
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_APP_PASSWORD")
    
    
    def generate_otp(self) -> str:
        return ''.join(random.choices(string.digits, k=5))
    
    def save_otp(self, email: str, otp: str, data: dict):
        expiration = datetime.now(timezone.utc) + timedelta(minutes=5)
        self._otp_store[email] = {
            'otp': otp,
            'expiration': expiration,
            'data': data.copy()
        }
        print(f"OTP guardado para {email}: {self._otp_store[email]}")
    
    def verify_otp(self, email: str, otp: str) -> Optional[dict]:
        stored = self._otp_store.get(email)
        if not stored:
            return None
        
        now = datetime.now(timezone.utc)
        print(f"Verificando OTP para {email}:")
        print(f"OTP almacenado: {stored['otp']}")
        print(f"OTP recibido: {otp}")
        print(f"Expiración: {stored['expiration']}")
        print(f"Hora actual: {now}")

        if now > stored['expiration']:
            print("OTP expirado")
            del self._otp_store[email]
            return None
        
        if stored['otp'] != otp:
            print("OTP no coincide")
            return None
        
        # Elimina el OTP y devuelve los datos almacenados
        data = stored['data']
        del self._otp_store[email]
        return data
    
    def send_otp_email(self, email: str, data: dict) -> tuple[bool, str]:
        try:
            otp = self.generate_otp()
            self.save_otp(email, otp, data)
            
            message = MIMEMultipart()
            message["From"] = self.smtp_username
            message["To"] = email
            message["Subject"] = "Código de verificación - Sistema de Gestión de Riesgos"
            
            body = f"""
            <html>
                <body>
                    <h2>Código de Verificación</h2>
                    <p>Tu código de verificación es: <strong>{otp}</strong></p>
                    <p>Este código expirará en 5 minutos.</p>
                    <p>Si no solicitaste este código, ignora este correo.</p>
                </body>
            </html>
            """
            
            message.attach(MIMEText(body, "html"))
            
            try: 
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls() # actualizar a TLS -> conexion segura
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(message)
            except SMTPConnectError as e:
                return False, f"Error al conectar al servidor SMTP: {str(e)}"
            except SMTPException as e:
                return False, f"Error al realizar la autenticación SMTP: {str(e)}"
            
            return True, "Código enviado exitosamente"
            
        except Exception as e:
            return False, f"Error al enviar el correo: {str(e)}"

    '''
    def can_resend_otp(self, email: str) -> Tuple[bool, Optional[int]]:
       stored = self._otp_store.get(email, {})
       if not stored or 'resend_time' not in stored:
           return True, None
       if datetime.now(timezone.now) < stored['resend_time']:
           return False, int((stored['resend_time'] - datetime.now(timezone.now)).total_seconds())
       return True, None
    '''
