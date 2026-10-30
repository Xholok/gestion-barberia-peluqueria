CREATE DATABASE IF NOT EXISTS barberia
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE barberia;

CREATE TABLE rol (
  id_rol INT AUTO_INCREMENT PRIMARY KEY,
  nombre_rol VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE persona (
  id_persona INT AUTO_INCREMENT PRIMARY KEY,
  nombres VARCHAR(80) NOT NULL,
  apellidos VARCHAR(80) NULL,
  telefono VARCHAR(15) NOT NULL
);

CREATE TABLE usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  id_persona INT NOT NULL UNIQUE,
  nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
  contrasena_hash VARCHAR(255) NOT NULL,
  id_rol INT NOT NULL,
  FOREIGN KEY (id_persona) REFERENCES persona(id_persona),
  FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE cliente (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  id_persona INT NOT NULL UNIQUE,
  usa_whatsapp BOOLEAN NOT NULL,
  observaciones VARCHAR(500) NULL,
  autoriza_datos BOOLEAN NOT NULL,
  fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_usuario_registro INT NOT NULL,
  FOREIGN KEY (id_persona) REFERENCES persona(id_persona),
  FOREIGN KEY (id_usuario_registro) REFERENCES usuario(id_usuario),
  CHECK (autoriza_datos = 1)
);

INSERT INTO rol (nombre_rol) VALUES
  ('administrador'), ('barbero'), ('peluquero');