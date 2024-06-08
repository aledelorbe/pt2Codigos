-- Creación de la Base de datos
CREATE DATABASE Sociodemografico;

USE Sociodemografico;

-- Creación de Entidades
CREATE TABLE Estado(
    id_estado INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(40) NOT NULL,
    CONSTRAINT PK_id_estado PRIMARY KEY (id_estado)
);

CREATE TABLE Escolaridad(
    id_escolaridad INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(40) NOT NULL,
    CONSTRAINT PK_id_escolaridad PRIMARY KEY (id_escolaridad)
);

CREATE TABLE Cancer(
    id_cancer INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(40) NOT NULL,
    CONSTRAINT PK_id_cancer PRIMARY KEY (id_cancer)
);

CREATE TABLE Ocupacion(
    id_ocupacion INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(90) NOT NULL,
    CONSTRAINT PK_id_ocupacion PRIMARY KEY (id_ocupacion)
);

-- Creación Relaciones
CREATE TABLE EstadoCancer(
    id_estado INT NOT NULL,
    id_cancer INT NOT NULL,
    cantidad INT NOT NULL,
    cluster INT NOT NULL,
    porcentaje FLOAT NOT NULL,
    CONSTRAINT FK_id_estado_can FOREIGN KEY (id_estado) REFERENCES Estado(id_estado),
    CONSTRAINT FK_id_cancer FOREIGN KEY (id_cancer) REFERENCES Cancer(id_cancer)
);

CREATE TABLE EstadoEscolaridad(
    id_estado INT NOT NULL,
    id_escolaridad INT NOT NULL,
    cantidad INT NOT NULL,
    cluster INT NOT NULL,
    porcentaje FLOAT NOT NULL,
    CONSTRAINT FK_id_estado_esco FOREIGN KEY (id_estado) REFERENCES Estado(id_estado),
    CONSTRAINT FK_id_escolaridad FOREIGN KEY (id_escolaridad) REFERENCES Escolaridad(id_escolaridad)
);

CREATE TABLE EstadoOcupacion(
    id_estado INT NOT NULL,
    id_ocupacion INT NOT NULL,
    cantidad INT NOT NULL,
    cluster INT NOT NULL,
    porcentaje FLOAT NOT NULL,
    CONSTRAINT FK_id_estado_ocu FOREIGN KEY (id_estado) REFERENCES Estado(id_estado),
    CONSTRAINT FK_id_ocupacion FOREIGN KEY (id_ocupacion) REFERENCES Ocupacion(id_ocupacion)
);
