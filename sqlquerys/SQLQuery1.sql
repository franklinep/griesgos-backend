USE master;
GO


CREATE DATABASE GRiesgosDB
ON 
-- Archivo de datos principal (MDF)
(NAME = GRiesgos_dat,    -- Nombre l�gico del archivo
 FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\GRiesgosdat.mdf',  -- Ubicaci�n f�sica
 SIZE = 10,           -- Tama�o inicial
 MAXSIZE = 50,        -- Tama�o m�ximo
 FILEGROWTH = 5)      -- Cu�nto crece cuando necesita m�s espacio

-- Archivo de registro (LDF) 
LOG ON
(NAME = GRiesgos_log,    -- Nombre l�gico del archivo de log
 FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\GRiesgos_log.ldf',
 SIZE = 5 MB,         -- Tama�o inicial del log
 MAXSIZE = 25 MB,     -- Tama�o m�ximo del log
 FILEGROWTH = 5 MB);  -- Incremento del log cuando se llena

GO     