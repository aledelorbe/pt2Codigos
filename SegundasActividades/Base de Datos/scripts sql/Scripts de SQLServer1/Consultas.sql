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







