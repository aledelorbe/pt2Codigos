
# METODOS Y DICCIONARIOS QUE SI SE MANDAN A LLAMAR FUERA DEL ARCHIVO

# Diccionarios con los colores para los 3 mapas
coloresMapaEstadoCancer = {
    "0": "#4682B4",
	"1": "#228B22",
	"2": "#FF4500",
	"3": "#FFD700", 
    "4": "#753a88" 
}
coloresMapaEstadoEducacion = {
    "0": "#4682B4",
	"1": "#228B22",
	"2": "#FF4500",
	"3": "#FFD700", 
    "4": "#753a88",
    "5": "#8A0707"
}
coloresMapaEstadoOcupacion = {
    "0": "#4682B4",
	"1": "#228B22",
	"2": "#FF4500",
	"3": "#FFD700", 
    "4": "#753a88" 
}
# 8A0707 rojo
# FF4500 naranja
# FFD700 amarillo
# 228B22 verde 
# 4682B4 azul
# 753a88 morado

# Para que cada estado se agrupe con su cluster correspondiente
gruposX = {
    "0": "Grupo 0",
	"1": "Grupo 1",
	"2": "Grupo 2",
	"3": "Grupo 3", 
    "4": "Grupo 4",
    "5": "Grupo 5" 
}

# Para calcular el centro de las areas geograficas
def calcular_centro_x(longitudes):
    return sum(longitudes) / len(longitudes)

def calcular_centro_y(latitudes):
    return sum(latitudes) / len(latitudes)

# Para corregir el problema de tener unos indices en el mapa y otros en la db (de mapa a db)
def corregirIndice(numero):
    if numero == 5:
        numero = 7
    elif numero == 6:
        numero = 8
    elif numero == 7:
        numero = 5
    elif numero == 8:
        numero = 6
    elif numero == 15:
        numero = 17
    elif numero == 16:
        numero = 15
    elif numero == 17:
        numero = 16

    return numero