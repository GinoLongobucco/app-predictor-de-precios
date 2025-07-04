# 🤖 Aplicación Web de Predicción de Precios de Libros

Este proyecto es una aplicación web funcional construida con Flask que utiliza un modelo de Machine Learning (Random Forest) para predecir el precio de un libro basándose en su título y calificación.

## Descripción

La aplicación encapsula un flujo de trabajo completo de ciencia de datos:

1.  **Recolección de Datos**: Un script extrae datos de miles de libros desde `books.toscrape.com`.
2.  **Entrenamiento de Modelo**: Un segundo script procesa estos datos, realiza ingeniería de características (incluyendo TF-IDF para el texto de los títulos) y entrena un modelo de regresión.
3.  **Inferencia en Tiempo Real**: La aplicación web carga el modelo entrenado y ofrece predicciones en tiempo real a través de una interfaz de usuario simple.

## Stack Tecnológico

- **Lenguaje**: Python
- **Librerías de ML/Datos**: Scikit-learn, Pandas, NumPy
- **Web Framework**: Flask
- **Web Scraping**: Requests, BeautifulSoup

## Cómo Ejecutar el Proyecto

Sigue estos pasos para poner en marcha la aplicación en tu máquina local.

### 1. Prerrequisitos

- Tener Python 3.8+ instalado.
- Tener Git instalado.

### 2. Instalación

Primero, clona el repositorio y navega al directorio del proyecto:

```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
```

Luego, crea un entorno virtual (recomendado) e instala las dependencias:

```bash
# Crear entorno virtual
python -m venv env

# Activar entorno (Windows)
# env\Scripts\activate
# Activar entorno (macOS/Linux)
# source env/bin/activate

# Instalar librerías
pip install -r requirements.txt
```

### 3. Ejecución (Secuencia de 3 Pasos)

Debes ejecutar los scripts en este orden para que la aplicación funcione:

**Paso 1: Recolectar los datos**
Este comando ejecuta el scraper y crea el archivo `data/biblioteca_completa.csv`.

```bash
python src/scraper.py
```

**Paso 2: Entrenar el modelo**
Este comando usa los datos recolectados para entrenar el modelo y guardar los artefactos en la carpeta `/models`.

```bash
python src/train_model.py
```

**Paso 3: Iniciar la aplicación web**
Este comando inicia el servidor de Flask.

```bash
flask run
```

Una vez iniciado, abre tu navegador y ve a **http://127.0.0.1:5000** para usar la aplicación.
