# app.py - tablero de mi proyecto (se publica el 19 de noviembre)
from pathlib import Path  # rutas de archivos
import pandas as pd  # tablas de datos
import solara  # tablero web
from matplotlib.figure import Figure  # grafico que Solara sabe mostrar

PREGUNTA = "¿El uso del telefono antes de dormir cambia las horas de sueno?"  # la pregunta del proyecto, terminada en signo de interrogacion
COLUMNA_FILTRO = "bedtime_phone_minutes"  # columna numerica de datos_proyecto.csv para el deslizador
ETIQUETA_FILTRO = "Uso del telefono antes de dormir"  # nombre de esa columna con su unidad
ETIQUETA_OBJETIVO = "sueño total en horas"  # nombre del objetivo con su unidad

CARPETA = Path(__file__).parent  # la carpeta donde vive este archivo
datos = pd.read_csv(CARPETA / 'datos_proyecto.csv')  # los datos del martes
resultado = pd.read_csv(CARPETA / 'resultado_proyecto.csv').iloc[0]  # lo que midio el martes
OBJETIVO = resultado['objetivo']  # lo que predice el modelo

def filtrar(tabla, columna, desde, hasta):
    # Devuelve solo las filas con la columna entre desde y hasta (incluidos).
    return tabla[tabla[columna].between(desde, hasta)]

def texto_resultado(res):
    # Frase honesta: el modelo comparado con la linea base, medido en datos no vistos.
    if res['metrica'] == 'MAE':
        return (f"Adivinar siempre el promedio se equivoca en promedio **{res['valor_linea_base']}**; "
                f"el modelo, **{res['valor_modelo']}**. Medido en {res['filas_test']} filas que el modelo no vio.")
    return (f"Decir siempre la clase mas comun acierta **{res['valor_linea_base']:.0%}**; "
            f"el modelo, **{res['valor_modelo']:.0%}**. Medido en {res['filas_test']} filas que el modelo no vio.")

def grafico(tabla, columna_x, columna_y, titulo, etiqueta_x, etiqueta_y):
    # Dispersion de dos columnas, con titulo y ejes rotulados.
    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.scatter(tabla[columna_x], tabla[columna_y], s=12, alpha=0.6)
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    return fig

minimo = float(datos[COLUMNA_FILTRO].min())
maximo = float(datos[COLUMNA_FILTRO].max())
rango = solara.reactive((minimo, maximo))  # estado: empieza con todo el rango

@solara.component
def Page():
    desde, hasta = rango.value  # el rango que eligio el usuario
    filtradas = filtrar(datos, COLUMNA_FILTRO, desde, hasta)
    solara.Title('Tablero del proyecto')
    solara.Markdown('## ' + PREGUNTA)
    solara.SliderRangeFloat(ETIQUETA_FILTRO, value=rango, min=minimo, max=maximo)
    solara.Markdown(f'Filas en el rango: **{len(filtradas)}** de {len(datos)}')
    if len(filtradas) == 0:
        solara.Markdown('**Ninguna fila cumple el filtro. Amplie el rango.**')
    else:
        solara.FigureMatplotlib(grafico(filtradas, COLUMNA_FILTRO, OBJETIVO, PREGUNTA,
                                        ETIQUETA_FILTRO, ETIQUETA_OBJETIVO))
    with solara.Card('Que tan bueno es el modelo'):
        solara.Markdown(texto_resultado(resultado))
