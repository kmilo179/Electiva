# Prediccion de Horas de Sueno segun Uso del Celular Nocturno

## URL publica
_[https://cd2026-mejia-jaimes.onrender.com](https://cd2026-mejia-jaimes.onrender.com)_

## Pregunta y decision
¿Como afecta el uso del telefono en minutos antes de dormir en las horas totales de sueño? Acá podrá explorar la relacion que hay entre el tiempo de pantalla nocturno y el descanso, y simular casos individuales con su margen de error para fomentar habitos saludables del sueño.

## Datos
Se utiliza el conjunto de datos `datos_proyecto.csv` que proviene de `bedtime_screentime_sleep_debt.csv` y registra los minutos de uso del celular antes de acostarse (`bedtime_phone_minutes`) como variable de entrada y las horas totales de sueno (`total_sleep_hours`) como variable objetivo.
link: https://www.kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits

## Limpieza
_Se verificó que los datos de cvs `bedtime_screentime_sleep_debt.csv` con 10625 filas, tuviera datos limpios, es decir cero datos:  nulos, duplicados, datos erroneos en las columnas analizadas `bedtime_phone_minutes` y `total_sleep_hours`_

## Modelo y evaluacion
Se entreno un Pipeline de regresion `modelo_proyecto.joblib` evaluado sobre 2125 filas de prueba (test) no vistas durante el entrenamiento. Utilizando el Error Absoluto Medio (MAE), el modelo obtuvo un error de **1.002** horas, frente a la linea base, cuyo error fue de **1.211** horas.

## Limitaciones
El modelo solo utiliza los minutos de uso del celular antes de dormir como predictor y es valido unicamente dentro del rango de minutos observado en los datos de entrenamiento.

## Como correrlo
conda activate cd2026
solara run app.py

## Uso de IA
_Se utilizo la ayuda de una Inteligencia Artificial, para verificar errores y entender el funcionamiento de distintas líneas de codigo._

## Explicacion de mi codigo
_1. Que hace el codigo: El sistema se divide en dos partes, primero es un cuaderno de entrenamiento y segundo es un tablero interactivo, esto se hace antes de procesarlo para evitar errores como fuga de datos, asegurando que los promedios se calculen solo con el grupo de entrenamiento.
    """
    X = datos[['bedtime_phone_minutes']]
    y = datos['total_sleep_hours']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"""
    
2. Luego calculamos primero una línea base sencilla que consiste en predecir siempre el promedio de horas de sueño del entrenamiento, lo que da un error de 1.211 horas en prueba, medimos el error de nuestro modelo entrenado sobre las mismas 2125 filas de prueba nunca vistas, obteniendo 1.002 horas.
    pred_base = [y_train.mean()] * len(y_test)
    mae_base = mean_absolute_error(y_test, pred_base)
    mae_modelo = mean_absolute_error(y_test, modelo.predict(X_test))
   
3. Y para finalizar, la función filtrar toma la tabla y deja solo las filas cuyos minutos de uso del celular están dentro del rango elegido en el deslizador. En Exploracion(), cada vez que el usuario mueve el control, el código cuenta cuántas filas quedaron en filtradas.
    @solara.component
    def Exploracion():
        desde, hasta = rango.value  # el rango que eligio el usuario
        filtradas = filtrar(datos, COLUMNA_FILTRO, desde, hasta)
        solara.SliderRangeFloat(ETIQUETA_FILTRO, value=rango, min=minimo, max=maximo)
        solara.Markdown(f'Filas en el rango: **{len(filtradas)}** de {len(datos)}')
        if len(filtradas) == 0:
            solara.Markdown('**Ninguna fila cumple el filtro. Amplie el rango.**')
        else:
            solara.FigureMatplotlib(grafico(filtradas, COLUMNA_FILTRO, OBJETIVO, PREGUNTA, ETIQUETA_FILTRO,             ETIQUETA_OBJETIVO))
    with solara.Card('Que tan bueno es el modelo'):
            solara.Markdown(texto_resultado(resultado))_

## Cambio Que le haría

Agregaría el cálculo dinámico del promedio de horas de sueño para las filas seleccionadas en el filtro, de modo que el usuario vea de inmediato cómo cambia el descanso promedio al ajustar el rango de minutos de pantalla. Para implementarlo, modificaría el `Exploracion()`: cuando `len(filtradas) > 0`, calcularía `promedio_sueno = filtradas[OBJETIVO].mean()` y lo mostraría junto al conteo de filas en el `solara.Markdown`.

