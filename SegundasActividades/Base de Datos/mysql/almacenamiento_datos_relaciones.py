# CARGA LAS LIBRERIAS
import pandas as pd
import accesoDb as db

# CARGAR LOS DF'S
dfEducaciones0_1 = pd.read_csv('Resul (0 - 1)/dfEducaciones.csv')
dfEmpleos0_1 = pd.read_csv('Resul (0 - 1)/dfEmpleos.csv')
dfEducaciones = pd.read_csv('Resul sin escala/dfEducaciones.csv')
dfEmpleos = pd.read_csv('Resul sin escala/dfEmpleos.csv')
gruposEducaciones = pd.read_csv('gruposEducaciones.csv')
gruposEmpleos = pd.read_csv('gruposEmpleos.csv')

# Determinacion de valores distintos
nombres = dfEducaciones.columns
nivelesEscolares = nombres[0:10]
canceres = nombres[10:]
nombres = dfEmpleos.columns
empleos = nombres[0:13]
estados = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 
           'Chihuahua', 'Coahuila de Zaragoza', 'Colima', 'Distrito Federal', 'Durango', 
           'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán de Ocampo', 'Morelos', 
           'México', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 
           'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 
           'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']

# PRUEBAS
# print(db.insertarEstadoParametro('escolaridad', 2, 2, 5, 7, 0.2))
# aux = db.buscarId('escolaridad', 'Hodgkin's Lymphoma')
# print(aux)
# print(db.insertarEstadoParametro('escolaridad', 1, 1, 4, 5, float(0.5627)))

contador = 0
# ITERA LOS DATOS DE ESTADO CON EDUCACION Y CON CANCER PARA SER ALMACENADOS
for rowEdu, rowEdu0_1, grupoEdu, estado in zip(dfEducaciones.values, dfEducaciones0_1.values, gruposEducaciones.values, estados):
    numCluster = int(grupoEdu[0])
    
    idEstado = db.buscarId('estado', estado)
    for i in range(10):
        cant = int(rowEdu[i])
        porcen = round(rowEdu0_1[i], 4)
        descrip = nivelesEscolares[i]
        print(estado, descrip, cant, numCluster, porcen)

        # Mandar a llamar el sp que inserta datos de estado con nivel escolar
        idEscolar = db.buscarId('escolaridad', descrip.rstrip())
        contador += db.insertarEstadoParametro('escolaridad', idEstado, idEscolar, cant, numCluster, float(porcen))

    for i in range(10, 46, 1):
        cant = int(rowEdu[i])
        porcen =  round(rowEdu0_1[i], 4)
        descrip = canceres[i - 10]
        print(estado, descrip, cant, numCluster, porcen)

        # Mandar a llamar el sp que inserta datos de estado con algun tipo de cancer
        idCancer = db.buscarId('cancer', descrip.rstrip())
        contador += db.insertarEstadoParametro('cancer', idEstado, idCancer, cant, numCluster, float(porcen))

# Solo si se hicieron las inserciones que se debieron hacer entonces...
if contador == 1472: # (32 estado x 36 tipos de cancer = 1152 registros) + 
                    # (32 estados x 10 niveles escolares = 320 registros) = 1472
    print(f'\nSe almacenaron correctamente los {contador} registros de estado con cancer y educacion.\n')
else:
    print(f'Datos almacenados: ', contador)
    print('Se almacenaron incorrectamente los datos de estado con cancer y educacion.')


contador = 0
# ITERAR LOS DATOS DEL ESTADO CON OCUPACION Y CON CANCER PARA SER ALMACENADOS
for rowEmp, rowEmp0_1, grupoEmp, estado in zip(dfEmpleos.values, dfEmpleos0_1.values, gruposEmpleos.values, estados):
    numCluster = int(grupoEmp[0])
    idEstado = db.buscarId('estado', estado)

    for i in range(13):
        cant = int(rowEmp[i])
        porcen = round(rowEmp0_1[i], 4)
        descrip = empleos[i]
        print(estado, descrip, cant, numCluster, porcen)
        # Mandar a llamar el sp que inserta datos de estado con nivel escolar
        idOcupacion = db.buscarId('ocupacion', descrip.rstrip())
        contador += db.insertarEstadoParametro('ocupacion', idEstado, idOcupacion, cant, numCluster, float(porcen))

# # Solo si se hicieron las inserciones que se debieron hacer entonces...
if contador == 416: # (32 estados x 13 categorias de empleo = 416 registros)  
                # Ya no se contemplaron los datos del cancer porque serian los mismos que ya se insertaron
    print(f'\nSe almacenaron correctamente los {contador} registros de estado con cancer y empleo.\n')
else:
    print('Se almacenaron incorrectamente los datos de estado con cancer y empleo.')



