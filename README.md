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
- `Unidad 1/Unidad 1 - Fundamentos de IA y Python.pptx`: diapositivas de apoyo para clase (34 diapositivas, un bloque por notebook), pensadas para exponer junto a los notebooks y como repaso para los estudiantes.



### Unidad 2 — Búsqueda en espacios de estados

- [Unidad 2/1_buscar-estados-ia.ipynb](Unidad%202/1_buscar-estados-ia.ipynb): representación formal de estados; **BFS**, **DFS** y **A\*** (heurística de Manhattan) sobre el **8-puzzle**.
- [Unidad 2/minimax-tictactoe/](Unidad%202/minimax-tictactoe/): aplicación **Streamlit** de Minimax en tres en raya (dificultad aleatoria, fácil y perfecta).
- `Unidad 2/Unidad 2 - Busqueda en Espacios de Estados.pptx`: diapositivas de apoyo para clase (21 diapositivas: representación de estados, BFS/DFS, A*/Voraz, comparación y Minimax), pensadas para exponer junto al notebook y la app, y como repaso para los estudiantes.

Para el demo:

```bash
cd "Unidad 2/minimax-tictactoe"
pip install -r requirements.txt
streamlit run app.py
```

Dependencias: `streamlit`, `matplotlib`, `pandas`.

### Unidad 3 — Machine Learning

Los notebooks están numerados en el orden narrativo en que se recorren; cada uno indica en su propio cierre cuál sigue.

- [Unidad 3/1-AI-fundamentals/](Unidad%203/1-AI-fundamentals/): fundamentos matemáticos y de preparación de datos para ML.
  - `1-algebra-lineal-ML.ipynb` — vectores, espacios vectoriales (base, dimensión, subespacios), normas y producto matriz-vector.
  - `2-gradiente-descendiente.ipynb` — descenso de gradiente, tasa de aprendizaje y mínimos locales (visualización 3D interactiva con Plotly).
  - `3-teorema-bayes.ipynb` — teorema de Bayes y la paradoja de las pruebas médicas.
  - `4-análisis-exploratorio-datos-EDA.ipynb` — EDA sobre el dataset Iris.
  - `5-data-preprocessing.ipynb` — imputación, outliers, escalado, codificación, PCA y validación cruzada evitando la fuga de datos entre entrenamiento y prueba.
  - `Demo EDA/` — EDA de punta a punta sobre estadísticas reales de jugadores de la NBA (temporada 2018-19), con *web scraping* y respaldo local (`nba2019.csv`).
- [Unidad 3/2-introduccion-machine-learning.ipynb](Unidad%203/2-introduccion-machine-learning.ipynb): recorrido completo del flujo de trabajo con `scikit-learn` sobre datasets simples (Iris, California Housing) — aprendizaje supervisado (regresión lineal, k-NN, Árboles de Decisión), no supervisado (K-Means), ensambles (Random Forest, XGBoost), AutoML con PyCaret, Grid Search y Randomized Search.
- [Unidad 3/3-aprendizaje-supervisado/](Unidad%203/3-aprendizaje-supervisado/) — regularización (Ridge, Lasso, ElasticNet), sobreajuste y curvas de aprendizaje sobre California Housing; Regresión Logística, SVM y comparación por validación cruzada sobre el dataset Wine.
- [Unidad 3/4-aprendizaje-no-supervisado.ipynb](Unidad%203/4-aprendizaje-no-supervisado.ipynb) — límites de K-Means frente a formas no convexas, DBSCAN, selección objetiva de k, clustering jerárquico y reducción de dimensionalidad con PCA (dataset Wine).
- [Unidad 3/5-modelos-ensamble.ipynb](Unidad%203/5-modelos-ensamble.ipynb) — bagging, Random Forest, boosting (AdaBoost, Gradient Boosting, XGBoost, LightGBM), voting y stacking (dataset Breast Cancer Wisconsin).
- [Unidad 3/6-pipelines-evaluacion.ipynb](Unidad%203/6-pipelines-evaluacion.ipynb) — `Pipeline` y `ColumnTransformer`, validación cruzada, métricas más allá de accuracy (ROC, precisión-recall) y manejo de clases desbalanceadas con SMOTE.
- `Unidad 3/Unidad 3 - Machine Learning.pptx`: diapositivas de apoyo para clase (41 diapositivas, un bloque por notebook), con 15 gráficas generadas reproduciendo el código real de cada notebook (descenso de gradiente, Bayes, EDA sobre Iris, outliers, fronteras de k-NN/SVM, regularización Ridge/Lasso, curvas de aprendizaje, sobreajuste de árboles, K-Means vs. DBSCAN, selección de k, comparación de ensambles y matriz de confusión), pensadas para exponer junto a los notebooks y como repaso para los estudiantes.



### Unidad 4 — IA moderna

Igual que en la Unidad 3, la numeración sigue el orden narrativo (de los fundamentos a las arquitecturas más avanzadas).

- [Unidad 4/1-fundamentos-redes-neuronales.ipynb](Unidad%204/1-fundamentos-redes-neuronales.ipynb): la neurona artificial, funciones de activación (sigmoid, tanh, ReLU, softmax), el ciclo de entrenamiento (pérdida, backpropagation, descenso de gradiente), un ejemplo completo con Keras sobre el dataset Digits, y sobreajuste/subajuste con una red real.
- [Unidad 4/2-vision-por-computador.ipynb](Unidad%204/2-vision-por-computador.ipynb): visión por computador clásica — imágenes como matrices, canales, convolución y filtrado con OpenCV, detección de bordes (Sobel, Canny) y binarización (umbral de Otsu).
- [Unidad 4/3-redes-convolucionales.ipynb](Unidad%204/3-redes-convolucionales.ipynb): CNN en profundidad — filtros aprendidos, mapas de activación, regularización con Dropout, aumento de datos y transferencia de aprendizaje con MobileNetV2.
- [Unidad 4/4-modelos-secuenciales.ipynb](Unidad%204/4-modelos-secuenciales.ipynb): RNN, LSTM y GRU sobre series de tiempo — por qué el gradiente que desaparece limita a las RNN simples, LSTM bidireccional y pronóstico multi-paso.
- [Unidad 4/5-procesamiento-lenguaje-natural.ipynb](Unidad%204/5-procesamiento-lenguaje-natural.ipynb): de TF-IDF a *embeddings* entrenables, con clasificación de sentimiento sobre reseñas de IMDB.
- [Unidad 4/6-transformers.ipynb](Unidad%204/6-transformers.ipynb): el mecanismo de *self-attention* calculado a mano, tokenización de subpalabras y pipelines preentrenados de Hugging Face.
- `Unidad 4/Unidad 4 - IA Moderna.pptx`: diapositivas de apoyo para clase (32 diapositivas, un bloque por notebook), con 21 gráficas reales extraídas directamente de las salidas ya ejecutadas de cada notebook (curvas de entrenamiento, matrices de confusión, filtros y mapas de activación de la CNN, comparación RNN/LSTM/GRU, matriz de atención, perplejidad, etc.), pensadas para exponer junto a los notebooks y como repaso para los estudiantes.


### Unidad 5 — Agentic AI

Igual que en las unidades 3 y 4, la numeración sigue el orden narrativo. Requiere un archivo `.env` en `Unidad 5/` con `GOOGLE_API_KEY` (no subas claves al repositorio).

- [Unidad 5/1-fundamentos-agentes.ipynb](Unidad%205/1-fundamentos-agentes.ipynb): qué es un agente de IA, el patrón **ReAct** y cómo construir uno con LangChain (`create_agent`) y Google Gemini.
- [Unidad 5/2-memoria-y-estado.ipynb](Unidad%205/2-memoria-y-estado.ipynb): memoria persistente entre turnos con el `checkpointer` de LangGraph, y aislamiento de conversaciones por `thread_id`.
- [Unidad 5/3-multiples-herramientas.ipynb](Unidad%205/3-multiples-herramientas.ipynb): un agente con varias herramientas distintas — cómo elige cuál usar, y cuándo no usar ninguna.
- [Unidad 5/4-grafos-langgraph.ipynb](Unidad%205/4-grafos-langgraph.ipynb): el grafo explícito (`StateGraph`, nodos, aristas condicionales) que `create_agent` construye por dentro.
- [Unidad 5/5-rag-como-herramienta.ipynb](Unidad%205/5-rag-como-herramienta.ipynb): recuperación aumentada por generación (RAG) integrada como una herramienta más del agente.
- [Unidad 5/6-multiagentes.ipynb](Unidad%205/6-multiagentes.ipynb): varios agentes especializados coordinados por un agente supervisor (patrón agentes-como-herramientas).
- [Unidad 5/7-evaluacion-de-agentes.ipynb](Unidad%205/7-evaluacion-de-agentes.ipynb): cómo medir si un agente elige bien sus herramientas (trayectoria) y responde correctamente (resultado).
- `Unidad 5/Unidad 5 - Agentic AI.pptx`: diapositivas de apoyo para clase (26 diapositivas, un bloque por notebook), con diagramas del patrón ReAct, enrutamiento de herramientas, el pipeline de RAG y la arquitectura supervisor-especialistas, además de transcripciones reales de conversaciones con los agentes y el grafo real de LangGraph — pensadas para exponer junto a los notebooks y como repaso para los estudiantes.



### Cheat Sheet

- [Cheat Sheet/Cheat Sheet.ipynb](Cheat%20Sheet/Cheat%20Sheet.ipynb): resumen de referencia rápida, transversal a todo el curso — sesgo y varianza, métricas de clasificación, PCA, teorema de Bayes, regresión, regularización, bloques y arquitecturas de CNN, ensambles, y estructuras de datos (pila, cola, árbol, grafo, tabla hash). No es una unidad nueva, sino un mapa de fórmulas y demostraciones visuales para consulta puntual.
- `Cheat Sheet/Cheat Sheet.pptx`: la misma referencia en formato de diapositivas (41 diapositivas, con las mismas figuras y tablas del notebook), pensada para exponer en sesiones de clase y como material de repaso para los estudiantes.

## Requisitos típicos

Varían por unidad. En conjunto aparecen: NumPy, Matplotlib, scikit-learn, XGBoost, LightGBM, imbalanced-learn, Plotly, TensorFlow/Keras, PyCaret, Streamlit, LangChain, LangGraph, `langchain-google-genai` y `python-dotenv`. Instálalos en el notebook (`%pip`) o en el entorno virtual.

## Licencia

[Apache License 2.0](LICENSE).