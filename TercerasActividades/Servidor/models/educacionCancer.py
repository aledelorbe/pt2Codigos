def datosEducacionCancer():
    eduGrupo0 = ['Guanajuato', 'Hidalgo', 'Morelos', 'Puebla', 'San Luis Potosí', 'Tlaxcala']
    eduGrupo1 = ['Baja California', 
                 'Baja California Sur', 
                 'Chihuahua', 
                 'Coahuila de Zaragoza', 
                 'Nuevo León', 
                 'Sonora', 
                 'Tamaulipas']
    eduGrupo2 = ['Campeche', 
                 'Guerrero', 
                 'Tabasco', 
                 'Veracruz de Ignacio de la Llave', 
                 'Yucatán']
    eduGrupo3 = ['Distrito Federal']
    eduGrupo4 = ['Aguascalientes', 'Durango', 'Jalisco']
    eduGrupo5 = ['México', 'Querétaro']
    eduGrupo6 = ['Chiapas', 'Oaxaca']
    eduGrupo7 = ['Quintana Roo']
    eduGrupo8 = ['Michoacán de Ocampo', 'Nayarit', 'Zacatecas']
    eduGrupo9 = ['Colima', 'Sinaloa']

    eduGrupos = [eduGrupo0, eduGrupo1, eduGrupo2, eduGrupo3, eduGrupo4, eduGrupo5, eduGrupo6, eduGrupo7, eduGrupo8, eduGrupo9]
    return eduGrupos

def formatoDatosEduCancer():
    listaListas = datosEducacionCancer()

    resultados = []
    for sublista in listaListas:
        if len(sublista) == 1:
            resultados.append(sublista[0])
        else:
            if len(sublista) == 2:
                resultados.append(sublista[0] + ' y ' + sublista[1])
            else:
                cadena = ''
                for elemento in sublista[:-2]:
                    cadena += elemento + ', '
                cadena += sublista[-2] + ' y ' + sublista[-1]
                resultados.append(cadena)

    return resultados