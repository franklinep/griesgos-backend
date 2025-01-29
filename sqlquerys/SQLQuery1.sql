USE master;
GO


CREATE DATABASE GRiesgosDB
ON 
-- Archivo de datos principal (MDF)
(NAME = GRiesgos_dat,    -- Nombre lógico del archivo
 FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\GRiesgosdat.mdf',  -- Ubicación física
 SIZE = 10,           -- Tamaño inicial
 MAXSIZE = 50,        -- Tamaño máximo
 FILEGROWTH = 5)      -- Cuánto crece cuando necesita más espacio

-- Archivo de registro (LDF) 
LOG ON
(NAME = GRiesgos_log,    -- Nombre lógico del archivo de log
 FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\GRiesgos_log.ldf',
 SIZE = 5 MB,         -- Tamaño inicial del log
 MAXSIZE = 25 MB,     -- Tamaño máximo del log
 FILEGROWTH = 5 MB);  -- Incremento del log cuando se llena

GO     