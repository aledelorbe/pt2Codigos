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
select id_estado, cluster
from EstadoCancer
group by id_estado, cluster
having cluster = 0
go

select sum(cantidad) as 'Total cluster 0'
from EstadoCancer
where cluster = 0
go

select sum(cantidad) as 'Total cluster 1'
from EstadoCancer
where cluster = 1
go

select sum(cantidad) as 'Total cluster 2'
from EstadoCancer
where cluster = 2
go

select sum(cantidad) as 'Total cluster 3'
from EstadoCancer
where cluster = 3
go

select sum(cantidad) as 'Total cluster 4'
from EstadoCancer
where cluster = 4
go

select *
from EstadoCancer
where cluster = 4






select e.id_estado, e.nombre, ec.cluster
from Estado e 
inner join EstadoCancer ec
on ec.id_estado = e.id_estado
group by e.id_estado, e.nombre, ec.cluster
having ec.cluster = 0
