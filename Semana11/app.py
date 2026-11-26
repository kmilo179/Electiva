# app.py - tablero de mi proyecto final (Solara). Se publica el 19 de noviembre.
PREGUNTA = "¿Como afecta el uso del telefono en minutos antes de dormir en las horas totales de sueño?"  # la pregunta del proyecto, terminada en signo de interrogacion
A_QUIEN = "Estudiantes, profesionales de la salud y los usuarios que quieran evaluar el tiempo de pantalla afecta su descanso."  # quien usa el tablero y que decide con el
COLUMNA_FILTRO = "bedtime_phone_minutes" # columna numerica de datos_proyecto.csv para el deslizador
ETIQUETA_FILTRO = "Uso del telefono antes de dormir (minutos)"  # nombre de esa columna con su unidad
ETIQUETA_OBJETIVO = "Horas totales de sueño (horas)"  # nombre del objetivo con su unidad
FUENTE = "https://www.kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits, Kagle es un enlace publico"  # enlace si es publico; origen y autorizacion si es privado
ETIQUETAS = { "bedtime_phone_minutes" : "Uso del telefono antes de dormir (minutos)"}  # diccionario {columna de entrada: nombre con unidad}

from pathlib import Path  # rutas de archivos
import joblib  # lee el modelo guardado
import pandas as pd  # tablas de datos
import solara  # tablero web
from matplotlib.figure import Figure  # grafico que Solara sabe mostrar

CARPETA = Path(__file__).parent  # rutas relativas: el servidor no tiene su disco
datos = pd.read_csv(CARPETA / 'datos_proyecto.csv')  # los datos del Taller 14
resultado = pd.read_csv(CARPETA / 'resultado_proyecto.csv').iloc[0]  # la evaluacion en test
modelo = joblib.load(CARPETA / 'modelo_proyecto.joblib')  # el modelo entrenado
OBJETIVO = resultado['objetivo']  # lo que predice el modelo
ENTRADAS = [col for col in datos.columns if col != OBJETIVO]  # todo menos el objetivo

def filtrar(tabla, columna, desde, hasta):
    # Devuelve solo las filas con la columna entre desde y hasta (incluidos). (Taller 15)
    return tabla[tabla[columna].between(desde, hasta)]

def texto_resultado(res):
    # Frase honesta: el modelo comparado con la linea base, medido en datos no vistos. (Taller 15)
    if res['metrica'] == 'MAE':
        return (f"Adivinar siempre el promedio se equivoca en promedio **{res['valor_linea_base']}**; "
                f"el modelo, **{res['valor_modelo']}**. Medido en {res['filas_test']} filas que el modelo no vio.")
    return (f"Decir siempre la clase mas comun acierta **{res['valor_linea_base']:.0%}**; "
            f"el modelo, **{res['valor_modelo']:.0%}**. Medido en {res['filas_test']} filas que el modelo no vio.")

def grafico(tabla, columna_x, columna_y, titulo, etiqueta_x, etiqueta_y):
    # Dispersion de dos columnas, con titulo y ejes rotulados. (Taller 15)
    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.scatter(tabla[columna_x], tabla[columna_y], s=12, alpha=0.6)
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    return fig
    
def grafico_hist_uso(tabla, columna_x, titulo, etiqueta_x):
    # Histograma de distribucion de uso del celular con titulo y ejes rotulados.
    fig = Figure(figsize=(6, 3.5))
    ax = fig.subplots()
    ax.hist(tabla[columna_x].dropna(), bins=20, color='steelblue', edgecolor='white')
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel('Numero de registros (personas)')
    return fig

def valor_tipico(serie):
    # Mediana si la columna es numerica; el valor mas comun si no lo es. (Parte 1)
    if pd.api.types.is_integer_dtype(serie):
        return int(round(serie.median()))
    if pd.api.types.is_numeric_dtype(serie):
        return float(serie.median())
    return serie.mode()[0]

def le_gana(res):
    # True si el modelo supera a la linea base en test. (Parte 3)
    if res['metrica'] == 'MAE':
        return res['valor_modelo'] < res['valor_linea_base']
    return res['valor_modelo'] > res['valor_linea_base']

def texto_prediccion(valor, res):
    # La prediccion de un caso con el error medido en test, en palabras del usuario. (Parte 3)
    if res['metrica'] == 'MAE':
        error = res['valor_modelo']
        return (f"El modelo estima **{valor:.1f}**. En {res['filas_test']} filas que no vio se equivoco en promedio "
                f"{error}: espere un valor entre **{valor - error:.1f}** y **{valor + error:.1f}**.")
    return (f"El modelo dice **{valor}**. En {res['filas_test']} filas que no vio acerto el {res['valor_modelo']:.0%}; "
            f"decir siempre la clase mas comun acierta el {res['valor_linea_base']:.0%}.")

def grafico_distribucion(tabla, columna, marca, titulo, etiqueta):
    # Como se reparten los valores de una columna, con el caso del usuario marcado en rojo. (Parte 4)
    fig = Figure(figsize=(6, 3))
    ax = fig.subplots()
    if pd.api.types.is_numeric_dtype(tabla[columna]):
        ax.hist(tabla[columna].dropna(), bins=20, color='lightgray')
        ax.axvline(marca, color='crimson', linewidth=2)
    else:
        conteo = tabla[columna].value_counts()
        ax.bar(conteo.index.astype(str), conteo.values, color=['crimson' if str(v) == str(marca) else 'lightgray' for v in conteo.index])
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta)
    ax.set_ylabel('Numero de filas')
    return fig

minimo = float(datos[COLUMNA_FILTRO].min())
maximo = float(datos[COLUMNA_FILTRO].max())
rango = solara.reactive((minimo, maximo))  # estado del filtro: empieza con todo el rango
caso = {col: solara.reactive(valor_tipico(datos[col])) for col in ENTRADAS}  # estado del caso: el tipico

def control(col):
    # Entrada de una columna que solo deja elegir valores que el modelo vio: no se rompe ni extrapola.
    serie, etiqueta = datos[col], ETIQUETAS.get(col, col)
    if pd.api.types.is_integer_dtype(serie):
        solara.SliderInt(etiqueta, value=caso[col], min=int(serie.min()), max=int(serie.max()))
    elif pd.api.types.is_numeric_dtype(serie):
        solara.SliderFloat(etiqueta, value=caso[col], min=float(serie.min()), max=float(serie.max()))
    else:
        solara.Select(etiqueta, value=caso[col], values=sorted(serie.dropna().unique().tolist()))

@solara.component
def Exploracion():
    desde, hasta = rango.value  # el rango que eligio el usuario
    filtradas = filtrar(datos, COLUMNA_FILTRO, desde, hasta)
    solara.SliderRangeFloat(ETIQUETA_FILTRO, value=rango, min=minimo, max=maximo)
    solara.Markdown(f'Filas en el rango: **{len(filtradas)}** de {len(datos)}')
    if len(filtradas) == 0:
        solara.Markdown('**Ninguna fila cumple el filtro. Amplie el rango.**')
    else:
        solara.FigureMatplotlib(grafico(filtradas, COLUMNA_FILTRO, OBJETIVO, PREGUNTA, ETIQUETA_FILTRO, ETIQUETA_OBJETIVO))
        solara.FigureMatplotlib(grafico_hist_uso(filtradas, COLUMNA_FILTRO, '¿Como se distribuye el tiempo de uso del celular antes de dormir?', ETIQUETA_FILTRO))
    with solara.Card('Que tan bueno es el modelo'):
        solara.Markdown(texto_resultado(resultado))

@solara.component
def VistaPrediccion():
    solara.Markdown('## Pruebe un caso')
    for col in ENTRADAS:
        control(col)  # una entrada acotada por columna
    tabla_caso = pd.DataFrame([{col: caso[col].value for col in ENTRADAS}])  # el caso, en una fila
    valor = modelo.predict(tabla_caso)[0]
    solara.Markdown(texto_prediccion(valor, resultado))
    if not le_gana(resultado):
        solara.Markdown('**Ojo: este modelo no le gana a la linea base. Tome la estimacion con cautela.**')
    solara.FigureMatplotlib(grafico_distribucion(datos, OBJETIVO, valor, 'Donde cae su caso frente a los datos?', ETIQUETA_OBJETIVO))

@solara.component
def Page():
    solara.Title('Tablero del proyecto')
    solara.Markdown('## ' + PREGUNTA)
    solara.Markdown('**Para quien:** ' + A_QUIEN)
    Exploracion()
    VistaPrediccion()
    solara.Markdown('**Fuente de los datos:** ' + FUENTE)
