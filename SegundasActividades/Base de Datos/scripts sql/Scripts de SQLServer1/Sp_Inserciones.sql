use Sociodemografico
go

-- Sp para insertar en la tabla 'EstadoCancer' ----------------------------------

CREATE OR ALTER PROCEDURE sp_insertarEstadoCancer 
	@estado varchar(40), @cancer varchar(40), @cantidad int, @cluster int
AS
BEGIN
	IF EXISTS(select id_estado from Estado where nombre = @estado) AND EXISTS(select id_cancer from Cancer where nombre = @cancer)
	BEGIN 		
		Declare @id_estado int, @id_cancer int;	

		set @id_estado = (select id_estado from Estado where nombre = @estado)
		set @id_cancer = (select id_cancer from Cancer where nombre = @cancer)

		INSERT INTO EstadoCancer VALUES (@id_estado, @id_cancer, @cantidad, @cluster);
	END
	ELSE
		PRINT('NO HUBO COINCIDENCIAS')	
END

-- Test del sp_insertarEstadoCancer
Exec sp_insertarEstadoCancer 'Aguascalientes', 'Bladder', 10, 1

select *
from EstadoCancer

DELETE FROM EstadoCancer


-- Sp para insertar en la tabla 'EstadoEscolaridad' ----------------------------------

CREATE OR ALTER PROCEDURE sp_insertarEstadoEscolaridad 
	@estado varchar(40), @escolaridad varchar(40), @cantidad int, @cluster int
AS
BEGIN
	IF EXISTS(select id_estado from Estado where nombre = @estado) AND EXISTS(select id_escolaridad from Escolaridad where nombre = @escolaridad)
	BEGIN 		
		Declare @id_estado int, @id_escolaridad int;	

		set @id_estado = (select id_estado from Estado where nombre = @estado)
		set @id_escolaridad = (select id_escolaridad from Escolaridad where nombre = @escolaridad)

		INSERT INTO EstadoEscolaridad VALUES (@id_estado, @id_escolaridad, @cantidad, @cluster);
	END
	ELSE
		PRINT('NO HUBO COINCIDENCIAS')	
END

-- Test del sp_insertarEstadoEscolariad
Exec sp_insertarEstadoEscolaridad 'Aguascalientes', 'Preescolar', 10, 1

select *
from EstadoEscolaridad

DELETE FROM EstadoEscolaridad


-- Sp para insertar en la tabla 'EstadoOcupacion' ----------------------------------

CREATE OR ALTER PROCEDURE sp_insertarEstadoOcupacion
	@estado varchar(40), @ocupacion varchar(90), @cantidad int, @cluster int
AS
BEGIN
	IF EXISTS(select id_estado from Estado where nombre = @estado) AND EXISTS(select id_ocupacion from Ocupacion where nombre = @ocupacion)
	BEGIN 		
		Declare @id_estado int, @id_ocupacion int;	

		set @id_estado = (select id_estado from Estado where nombre = @estado)
		set @id_ocupacion = (select id_ocupacion from Ocupacion where nombre = @ocupacion)

		INSERT INTO EstadoOcupacion VALUES (@id_estado, @id_ocupacion, @cantidad, @cluster);
	END
	ELSE
		PRINT('NO HUBO COINCIDENCIAS')	
END

-- Test del sp_insertarEstadoOcupacion
Exec sp_insertarEstadoOcupacion 'Aguascalientes', 'Comerciantes, empleados en ventas y agentes de ventas', 12, 6

select *
from EstadoOcupacion

DELETE FROM EstadoOcupacion