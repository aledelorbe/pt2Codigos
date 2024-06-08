def datosEmpleoCancer():
    empGrupo0 = ['Hidalgo', 'San Luis Potosí']
    empGrupo1 = ['Chihuahua', 'Coahuila de Zaragoza', 'Colima', 'Durango', 'Sonora', 'Tamaulipas']
    empGrupo2 = ['Guerrero', 'Tabasco', 'Veracruz de Ignacio de la Llave']
    empGrupo3 = ['México', 'Querétaro']
    empGrupo4 = ['Quintana Roo']
    empGrupo5 = ['Aguascalientes', 'Guanajuato', 'Jalisco', 'Morelos']
    empGrupo6 = ['Baja California', 'Baja California Sur', 'Nuevo León']
    empGrupo7 = ['Chiapas', 'Oaxaca']
    empGrupo8 = ['Campeche', 'Yucatán']
    empGrupo9 = ['Distrito Federal']
    empGrupo10 = ['Michoacán de Ocampo', 'Nayarit', 'Zacatecas']
    empGrupo11 = ['Puebla', 'Tlaxcala']
    empGrupo12 = ['Sinaloa']

    empGrupos = [empGrupo0, empGrupo1, empGrupo2, empGrupo3, empGrupo4, empGrupo5, empGrupo6, empGrupo7, empGrupo8, empGrupo9, empGrupo10, empGrupo11, empGrupo12]
    return empGrupos


def formatoDatosEmpCancer():
    listaListas = datosEmpleoCancer()

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