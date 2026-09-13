def reconciliar_columna(columna_cruda, tipo_destino):
    """
    Recibe una columna sucia (lista de strings) y el tipo al que debe convertirse
    (la propia funcion int o float de Python, pasada como valor).
    Devuelve una lista nueva, mas corta o igual, ya convertida a tipo_destino:
      - descarta los valores 'n/d' (no los convierte en 0),
      - repara la coma decimal antes de convertir (.replace(',', '.')),
      - convierte cada valor restante con tipo_destino(valor).
    """
    columna_limpia = []
    for valor in columna_cruda:
        if valor == 'n/d':
            continue
        else:
            #valor.replace(',', '.')
            columna_limpia.append(tipo_destino(valor.replace(',', '.')))
        
        # TODO 2 -- Ahora usted: escriba aqui el cuerpo del for.
        #   Reutilice la logica de la Parte 2 de la semana 3:
        #   1) si valor == 'n/d', descartelo (continue) sin agregarlo a columna_limpia
        #   2) si no, repare la coma con .replace(',', '.')
        #   3) conviertalo con tipo_destino(...) y agreguelo a columna_limpia con .append(...)
        #pass  # <-- reemplace esta linea

    # El contenido de la funcion, verificado automaticamente cada vez que se llama:
    assert len(columna_limpia) <= len(columna_cruda), 'no puede sobrar mas datos limpios que crudos'
    assert all(isinstance(v, tipo_destino) for v in columna_limpia), 'todo debe quedar en el tipo pedido'
    assert len(columna_limpia) > 0, 'La lista columna_limpia debe tener más de 0 valores'
    return columna_limpia