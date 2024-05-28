
# METODOS Y DICCIONARIOS QUE SI SE MANDAN A LLAMAR FUERA DEL ARCHIVO

# Diccionarios con los colores para los 3 mapas
coloresEducacion = {
    "0": "#4682B4", # Azul metalico
	"1": "#FF4500", # Naranja
	"2": "#C71585", # Rosa Oscuro
	"3": "#006847", # Verde bandera
    "4": "#753a88", # Morado oscuro
    "5": "#8B4513", # Cafe
    "6": "#FF0000", # Rojo
    "7": "#00FF00", # Verde lima
    "8": "#FFFF00", # Amarillo
    "9": "#00FFFF", # Cian
}
coloresOcupacion = {
    "0": "#4682B4", # Azul metalico
	"3": "#FF4500", # Naranja
	"6": "#C71585", # Rosa Oscuro
	"1": "#006847", # Verde bandera
    "4": "#753a88", # Morado oscuro
    "5": "#8B4513", # Cafe
    "2": "#FF0000", # Rojo
    "7": "#00FF00", # Verde lima
    "8": "#FFFF00", # Amarillo
    "9": "#00FFFF", # Cian
    "10": "#FF69B4", # Rosa metalico
    "11": "#1A195D", # Azul marino
    "12": "#B22222", # Rojo metalico
}

# Para que cada estado se agrupe con su cluster correspondiente
gruposX = {
    "0": "Grupo 1",
	"1": "Grupo 2",
	"2": "Grupo 3",
	"3": "Grupo 4", 
    "4": "Grupo 5",
    "5": "Grupo 6",
    "6": "Grupo 7",
	"7": "Grupo 8",
	"8": "Grupo 9", 
    "9": "Grupo 10",
    "10": "Grupo 11",
	"11": "Grupo 12", 
    "12": "Grupo 13",
}

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