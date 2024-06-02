# Csv:
# https://drive.google.com/file/d/1d0P1elh1B3lX9g3tE981ZWpZLRl9zAt_/view

# Importar librerias
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

dataSet = pd.read_csv('Mall_Customers.csv') # Cargar los datos
print(dataSet.isna().any()) # Ver si alguna columna tiene valores faltantes

# Imprime el valor maximo y minimo de cada columna
for columna in dataSet.columns:
    print(f'Columna: {columna}')
    print(f'\tValor maximo: {dataSet[columna].max()}')
    print(f'\tValor minimo: {dataSet[columna].min()}')

X = dataSet.iloc[:, 3:5].values # Seleccion de caracteristicas
# Las caraacteristicas seleccionadas estan en mas o menos el mismo rango y
# se observo que no hay valores faltantes, por lo que no se aplica algun 
# escalamiento o normalizacion.

# GRAFICACION DE DATOS
plt.figure(figsize=(10, 6))
plt.title('Datos')
plt.scatter(X[:, 0], X[:, 1])

# METODO DEL CODO
wcss = [] # Declaracion de la lista que almacenara las inercias.
cantidadClusters = 11
for i in range(1, cantidadClusters):
    algoritmoKmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 100, random_state = 0)
    algoritmoKmeans.fit(X)
    wcss.append(algoritmoKmeans.inertia_)

# Grafico del codo
plt.figure(figsize=(10, 6))
plt.title('Metodo del codo')
plt.plot(range(1, cantidadClusters), wcss)
plt.scatter(range(1, cantidadClusters), wcss, s = 20)
plt.xticks(range(1, cantidadClusters), range(1, cantidadClusters))
plt.ylabel('WCSS')
plt.xlabel('Numero de clusters')
plt.grid()

# Al observar el grafico del codo y de acuerdo a la literatura esta nos dice
# que el numero optimo de clusters es aquel valor el cual es el ultimo en disminuir
# drasticamente. Con lo cual, se concluye que para este caso en especifico el numero
# de clusters optimo es: 5. 

# ALGORITMO K-MEANS
algoritmoKmeans = KMeans(n_clusters = 5, init = 'k-means++', max_iter = 100, random_state = 0)
algoritmoKmeans.fit(X)
y = algoritmoKmeans.fit_predict(X)

# Graficar los baricentros de los clusters
plt.figure(figsize=(10, 6))
plt.title('K-MEANS')
plt.scatter(algoritmoKmeans.cluster_centers_[:, 0], algoritmoKmeans.cluster_centers_[:, 1], c = 'yellow', marker = 'd', label = 'Baricentros')

# Graficar los datos que pertenecen a cada cluster
plt.scatter(X[y == 0, 0], X[y == 0, 1], c = 'blue', label = 'cluster 1')
plt.scatter(X[y == 1, 0], X[y == 1, 1], c = 'red', label = 'cluster 2')
plt.scatter(X[y == 2, 0], X[y == 2, 1], c = 'purple', label = 'cluster 3')
plt.scatter(X[y == 3, 0], X[y == 3, 1], c = 'green', label = 'cluster 4')
plt.scatter(X[y == 4, 0], X[y == 4, 1], c = 'brown', label = 'cluster 5')
plt.xlabel('Caracteristica 1 (Ingreso anual)')
plt.ylabel('Caracteristica 2 (Puntuacion generada)')
plt.legend(loc = 5)
plt.show()