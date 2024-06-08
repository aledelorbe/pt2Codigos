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

-- Para saber el no total de personas con cancer
select e.id_estado, e.nombre, sum(ec.cantidad) --, sum(ec.porcentaje) 
from EstadoCancer ec
inner join Estado e
on e.id_estado = ec.id_estado
group by e.id_estado, e.nombre
order by 1

-- Para saber el nombre de los estados en el grupo X (educacion)
select nombre
from estado
where id_estado in (select distinct(id_estado)
					from EstadoEscolaridad
					where cluster = 1)

-- Para saber el nombre de los estados en el grupo X (empleo)
select nombre
from estado
where id_estado in (select distinct(id_estado)
					from EstadoOcupacion
					where cluster = 1)

