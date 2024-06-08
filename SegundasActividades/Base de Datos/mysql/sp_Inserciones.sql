-- Usar la base de datos Sociodemografico
USE Sociodemografico;

-- Procedimiento almacenado para insertar en la tabla 'EstadoCancer'
DELIMITER //
CREATE PROCEDURE sp_insertarEstadoCancer(
    IN n_estado VARCHAR(40), 
    IN n_cancer VARCHAR(40), 
    IN n_cantidad INT, 
    IN n_cluster INT, 
    IN f_porcentaje FLOAT
)
BEGIN
    DECLARE d_id_estado INT;
    DECLARE d_id_cancer INT;

    IF EXISTS(SELECT id_estado FROM Estado WHERE nombre = n_estado) AND EXISTS(SELECT id_cancer FROM Cancer WHERE nombre = n_cancer) THEN
        SET d_id_estado = (SELECT id_estado FROM Estado WHERE nombre = n_estado);
        SET d_id_cancer = (SELECT id_cancer FROM Cancer WHERE nombre = n_cancer);

        INSERT INTO EstadoCancer
        VALUES (d_id_estado, d_id_cancer, n_cantidad, n_cluster, f_porcentaje);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NO HUBO COINCIDENCIAS';
    END IF;
END //
DELIMITER ;

-- Test del sp_insertarEstadoCancer
CALL sp_insertarEstadoCancer('Aguascalientes', 'Bladder', 10, 1, 0.2456);

SELECT * FROM EstadoCancer;
-- solamente truncando en la interfaz grafica


-- Procedimiento almacenado para insertar en la tabla 'EstadoEscolaridad'
DELIMITER //
CREATE PROCEDURE sp_insertarEstadoEscolaridad(
    IN n_estado VARCHAR(40), 
    IN n_escolaridad VARCHAR(40), 
    IN n_cantidad INT, 
    IN n_cluster INT, 
    IN n_porcentaje FLOAT
)
BEGIN
    DECLARE d_id_estado INT;
    DECLARE d_id_escolaridad INT;

    IF EXISTS(SELECT id_estado FROM Estado WHERE nombre = n_estado) AND EXISTS(SELECT id_escolaridad FROM Escolaridad WHERE nombre = n_escolaridad) THEN
        SET d_id_estado = (SELECT id_estado FROM Estado WHERE nombre = n_estado);
        SET d_id_escolaridad = (SELECT id_escolaridad FROM Escolaridad WHERE nombre = n_escolaridad);

        INSERT INTO EstadoEscolaridad
        VALUES (d_id_estado, d_id_escolaridad, n_cantidad, n_cluster, n_porcentaje);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NO HUBO COINCIDENCIAS';
    END IF;
END //
DELIMITER ;

-- Test del sp_insertarEstadoEscolaridad
CALL sp_insertarEstadoEscolaridad('Aguascalientes', 'Preescolar', 10, 1, 0.5124);

SELECT * FROM EstadoEscolaridad;
-- solamente truncando en la interfaz grafica


-- Procedimiento almacenado para insertar en la tabla 'EstadoOcupacion'
DELIMITER //
CREATE PROCEDURE sp_insertarEstadoOcupacion(
    IN n_estado VARCHAR(40), 
    IN n_ocupacion VARCHAR(90), 
    IN n_cantidad INT, 
    IN n_cluster INT, 
    IN n_porcentaje FLOAT
)
BEGIN
    DECLARE d_id_estado INT;
    DECLARE d_id_ocupacion INT;

    IF EXISTS(SELECT id_estado FROM Estado WHERE nombre = n_estado) AND EXISTS(SELECT id_ocupacion FROM Ocupacion WHERE nombre = n_ocupacion) THEN
        SET d_id_estado = (SELECT id_estado FROM Estado WHERE nombre = n_estado);
        SET d_id_ocupacion = (SELECT id_ocupacion FROM Ocupacion WHERE nombre = n_ocupacion);

        INSERT INTO EstadoOcupacion
        VALUES (d_id_estado, d_id_ocupacion, n_cantidad, n_cluster, n_porcentaje);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NO HUBO COINCIDENCIAS';
    END IF;
END //
DELIMITER ;

-- Test del sp_insertarEstadoOcupacion
CALL sp_insertarEstadoOcupacion('Aguascalientes', 'Comerciantes, empleados en ventas y agentes de ventas', 12, 6, 0.3465);

SELECT * FROM EstadoOcupacion;
-- solamente truncando en la interfaz grafica
