-- Creacion de la Base de datos
create database Sociodemografico
go

use Sociodemografico
go

-- Creacion de Entidades
create table Estado(
	id_estado int not null identity(1,1),
	nombre varchar(40),

	constraint PK_id_estado primary key (id_estado)
)
go

create table Escolaridad(
	id_escolaridad int not null identity(1,1),
	nombre varchar(40),

	constraint PK_id_escolaridad primary key (id_escolaridad)
)
go

create table Cancer(
	id_cancer int not null identity(1,1),
	nombre varchar(40),

	constraint PK_id_cancer primary key (id_cancer)
)
go

create table Ocupacion(
	id_ocupacion int not null identity(1,1),
	nombre varchar(90),

	constraint PK_id_ocupacion primary key (id_ocupacion)
)
go

-- Creacion Relaciones
create table EstadoCancer(
	id_estado int not null,
	id_cancer int not null,
	cantidad int,
	--anio varchar(6),

	constraint FK_id_estado_can foreign key (id_estado) references Estado(id_estado),
	constraint FK_id_cancer foreign key (id_cancer) references Cancer(id_cancer)
)
go

create table EstadoEscolaridad(
	id_estado int not null,
	id_escolaridad int not null,
	cantidad int,
	--anio varchar(6),

	constraint FK_id_estado_esco foreign key (id_estado) references Estado(id_estado),
	constraint FK_id_escolaridad foreign key (id_escolaridad) references Escolaridad(id_escolaridad)
)
go

create table EstadoOcupacion(
	id_estado int not null,
	id_ocupacion int not null,
	cantidad int,
	--anio varchar(6),

	constraint FK_id_estado_ocu foreign key (id_estado) references Estado(id_estado),
	constraint FK_id_ocupacion foreign key (id_ocupacion) references Ocupacion(id_ocupacion)
)
go