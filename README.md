# IA Course UdB

Contenido teórico-práctico de la asignatura **Inteligencia Artificial** del programa de Ingeniería de Sistemas de la **Universidad de Boyacá**.

La parte práctica vive en este repositorio (notebooks Jupyter y un demo interactivo). La teoría de cada unidad está en el sitio del curso:

**[AI UdB Course](https://ai-course-udb.my.canva.site/#home)**

2026

## Cómo usar este repositorio

1. Clona el repositorio.
2. Instala Python 3.12 (o similar) y un entorno (Anaconda/`conda` o [uv](https://docs.astral.sh/uv/)). La Unidad 1 incluye una guía de instalación en `Unidad 1/1_Introducción.ipynb`.
3. Abre los notebooks en **VS Code / Cursor** o **Jupyter**. Selecciona el kernel del entorno virtual.
4. Ejecuta las celdas con `Shift + Enter`.

Cada unidad asume que ya viste el material correspondiente en el sitio Canva.

## Estructura del curso



### Unidad 1 — Introducción y fundamentos de Python

- [Unidad 1/1_Introducción.ipynb](Unidad%201/1_Introducción.ipynb): definiciones de IA, tipos (ML, DL, LLM, IAG), lenguajes, frameworks y entornos; instalación de Anaconda y `uv`.
- [Unidad 1/fundamentos/](Unidad%201/fundamentos/):
  - `1_notebooks.ipynb` — Jupyter en VS Code (celdas, kernel, markdown).
  - `2_python_basics.ipynb` — Python básico (tipos, estructuras, control de flujo, funciones).
  - `3_python_intermedio.ipynb` — comprensiones, generadores, type hints, decoradores.
  - `4_async_python.ipynb` — programación asíncrona.
  - `5_pydantic.ipynb` — validación de datos y salida de un LLM.



### Unidad 2 — Búsqueda en espacios de estados

- [Unidad 2/1_buscar-estados-ia.ipynb](Unidad%202/1_buscar-estados-ia.ipynb): representación formal de estados; **BFS**, **DFS** y **A\*** (heurística de Manhattan) sobre el **8-puzzle**.
- [Unidad 2/taller_u2.ipynb](Unidad%202/taller_u2.ipynb): taller de evacuación / vehículo autónomo (espacio de estados, algoritmos, rúbrica). Entrega: notebook + carpeta `assets` en un comprimido.
- [Unidad 2/minimax-tictactoe/](Unidad%202/minimax-tictactoe/): aplicación **Streamlit** de Minimax en tres en raya (dificultad aleatoria, fácil y perfecta).

Para el demo:

```bash
cd "Unidad 2/minimax-tictactoe"
pip install -r requirements.txt
streamlit run app.py
```

Dependencias: `streamlit`, `matplotlib`, `pandas`.

### Unidad 3 — Machine Learning

- [Unidad 3/1_ML_implementation.ipynb](Unidad%203/1_ML_implementation.ipynb): aprendizaje supervisado (regresión lineal, California Housing, k-NN, árboles), no supervisado (K-Means), ensambles (Random Forest, XGBoost), AutoML con PyCaret, Grid Search y Randomized Search.
- [Unidad 3/slides demo/](Unidad%203/slides%20demo/): demos de álgebra lineal, gradiente descendente, teorema de Bayes, EDA y preprocesamiento.
- [Unidad 3/recursos/](Unidad%203/recursos/): cálculo de probabilidades (`1-calculo-probabilidades.ipynb`), EDA en Python (`2-python-EDA.ipynb`) y dataset `nba2019.csv`.



### Unidad 4 — IA moderna

- [Unidad 4/IA_Moderna.ipynb](Unidad%204/IA_Moderna.ipynb): ANN con Keras/TensorFlow (Iris), CNN, RNN/LSTM y Transformers.
- [Unidad 4/computer-vision.ipynb](Unidad%204/computer-vision.ipynb): visión por computador clásica — imágenes como matrices, canales, convolución y filtrado con OpenCV.



### Unidad 5 — Agentic AI

- [Unidad 5/agent-ai.ipynb](Unidad%205/agent-ai.ipynb): agente **ReAct** con LangChain y Google Gemini (herramienta de cálculo). Requiere un archivo `.env` con `GOOGLE_API_KEY` (no subas claves al repositorio).



## Requisitos típicos

Varían por unidad. En conjunto aparecen: NumPy, Matplotlib, scikit-learn, TensorFlow/Keras, PyCaret, XGBoost, Streamlit, LangChain, `langchain-google-genai` y `python-dotenv`. Instálalos en el notebook (`%pip`) o en el entorno virtual.

## Licencia

[Apache License 2.0](LICENSE).