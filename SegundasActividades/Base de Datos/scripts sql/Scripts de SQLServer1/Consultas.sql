use Sociodemografico
go 

-- Consultas de los catalogos ----------------------------------------
select *
from Escolaridad
go

select *
from Estado
go

select *
from Cancer
go

select *
from Ocupacion
go

-- Consultas de las relaciones ----------------------------------------
select *
from EstadoCancer
go

select *
from EstadoOcupacion
go

select *
from EstadoEscolaridad
go


-- Consultas para determinar que representa cada grupo
select e.id_estado, e.nombre, ec.cluster
from Estado e 
inner join EstadoCancer ec
on ec.id_estado = e.id_estado
group by e.id_estado, e.nombre, ec.cluster
having ec.cluster = 4 -- los estados en cierto cluster

select sum(cantidad) as 'Total'
from EstadoCancer
where cluster = 0
go -- Total de personas con algun tipo de cancer en cierto cluster

SELECT id_estado, cluster, sum(cantidad) AS 'cantidad de personas'
FROM EstadoCancer
GROUP BY id_estado, cluster
order by 1 -- Cantidad de personas con algun tipo cancer en cada estado

SELECT cluster, avg(cantidad) AS 'promedio de cantidad de personas'
FROM EstadoCancer
GROUP BY cluster
order by 1 --


------------------------
select e.id_estado, e.nombre, ec.cluster
from Estado e 
inner join EstadoOcupacion ec
on ec.id_estado = e.id_estado
group by e.id_estado, e.nombre, ec.cluster
having ec.cluster = 2



-- Para consultar en la tabla 'EstadoCancer' ---------------------------------------

select e.nombre, ec.cluster, c.nombre, ec.cantidad  
from EstadoCancer ec
inner join Estado e
on e.id_estado = ec.id_estado
inner join Cancer c
on c.id_cancer = ec.id_cancer
where e.id_estado = 1 -- 36 tipos de cancer


-- Para consultar en la tabla 'EstadoEscolaridad' ----------------------------------

select e.nombre, ee.cluster, esc.nombre, ee.cantidad  
from EstadoEscolaridad ee
inner join Estado e
on e.id_estado = ee.id_estado
inner join Escolaridad esc
on esc.id_escolaridad = ee.id_escolaridad
where e.id_estado = 1 -- 10 niveles escolares


-- Para consultar en la tabla 'EstadoEscolaridad' ----------------------------------

select e.nombre, ee.cluster, esc.nombre, ee.cantidad  
from EstadoOcupacion ee
inner join Estado e
on e.id_estado = ee.id_estado
inner join Ocupacion esc
on esc.id_ocupacion = ee.id_ocupacion
where e.id_estado = 1 -- 13 categorias de ocupacion





