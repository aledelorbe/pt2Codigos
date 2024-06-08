USE Sociodemografico;

-- Consultas de los catálogos ----------------------------------------
SELECT *
FROM Escolaridad;

SELECT *
FROM Estado;

SELECT *
FROM Cancer;

SELECT *
FROM Ocupacion;

-- Consultas de las relaciones ----------------------------------------
SELECT count(*)
FROM EstadoCancer;

SELECT count(*)
FROM EstadoOcupacion;

SELECT count(*)
FROM EstadoEscolaridad;

-- Para saber el no total de personas con cáncer
SELECT e.id_estado, e.nombre, SUM(ec.cantidad) --, SUM(ec.porcentaje) 
FROM EstadoCancer ec
INNER JOIN Estado e
ON e.id_estado = ec.id_estado
GROUP BY e.id_estado, e.nombre
ORDER BY 1;
