    contador = 0
    # ITERAR LOS DATOS DEL ESTADO CON CANCER PARA SER ALMACENADOS
    for index, row in dfEstados.iterrows():
        estado = row["estado"]
        numCluster = int(gruposCanceres.iloc[index].values)
        print(f'Índice: {index}, Estado: {estado}, numCluster: {numCluster}')
        for i in range(0, 72, 2): # 36*2 = 72. 36 tipos de cancer y de 2 en dos.
            descrip = dfEstados.iloc[index, 1 + i]
            cant = int(dfEstados.iloc[index, 2 + i])
            print(f'Descrip: {descrip}, Cant: {cant}')
            # Mandar a llamar el sp que inserta datos de estado con cancer
            cursor.execute("{CALL sp_insertarEstadoCancer (?, ?, ?, ?)}", (estado, descrip, cant, numCluster))
            if cursor.rowcount == 1:
                contador += 1
    
    # Solo si se hicieron las inserciones que se debieron hacer entonces...
    if contador == 1152: # 32 estado x 36 tipos de cancer = 1152 registros
        print('Se almacenaron correctamente los datos de estado con cancer.')
        # Guardar las inserciones realizadas.
        conn.commit()
    else:
        print('Se almacenaron incorrectamente los datos de estado con cancer.')
        # Deshacer todo lo que se haya hecho en la db
        conn.rollback()