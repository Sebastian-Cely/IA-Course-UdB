# Hoja de ruta de ajustes — IA-Course-UdB

Lista de hallazgos de la revisión del repositorio (2026-09-05), para ir resolviendo uno por uno.
Marca `[x]` cuando un ítem quede corregido.

## A. Transversales (afectan todo el repo)

- [x] **A1.** README — enlaces markdown envueltos en backticks (` `[texto](ruta)` `), quedan como texto literal en vez de clicables. Afecta líneas 14, 26-27, 38-40, 54-56, 62, 68.
- [x] **A2.** Guía de instalación (`Unidad 1/1_Introducción.ipynb`) solo cubre Windows (PowerShell/Anaconda Prompt/.exe). Falta el equivalente para macOS/Linux.
- [x] **A3.** `requirements.txt` en UTF-16LE (artefacto de PowerShell) en vez de UTF-8: `Unidad 1/requirements.txt`, `Unidad 1/fundamentos/requirements.txt`, `Unidad 2/requirements.txt`, `Unidad 3/requirements.txt`, `Unidad 3/slides demo/requirements.txt`, `Unidad 3/recursos/requirements.txt`, `Unidad 5/requirements.txt`. *(Corrección: el contenido de estos archivos sí era correcto — cada uno corresponde a los imports reales de su carpeta; `Unidad 3/requirements.txt` raíz ya tenía scikit-learn/xgboost/pycaret. Solo se convirtió la codificación a UTF-8, sin tocar el contenido.)*
- [x] **A4.** `.gitignore` con reglas muertas (`u1/`, `fundam/`, `u2/`, `u3/`, `u3rec/`, `u3slides/`, `u4/`, `u5/`, `pycaret/`, `slides/`) que no coinciden con las carpetas reales (`Unidad 1/`, etc.). *(Eliminadas.)*
- [x] **A5.** Falta `.DS_Store` en `.gitignore` (hay 3 archivos sin trackear: raíz, Unidad 1, Unidad 3).
- [x] **A6.** `Unidad 3/mejor_modelo_pycaret.pkl` está trackeado en git pese a que la regla `pycaret/` sugiere que no debería estarlo. *(Es un artefacto regenerable por `save_model()`/`load_model()` en el notebook — se hizo `git rm --cached` y se agregó `*.pkl` a `.gitignore`. Queda como cambio staged, sin commitear.)*
- [x] **A7.** `Unidad 4/computer-vision.ipynb` no aparece en el README (Unidad 4 solo menciona `IA_Moderna.ipynb`). Tampoco se menciona `2-python-EDA.ipynb` en la descripción de Unidad 3.
- [x] **A8.** README línea 38: "A" en vez de "A\*" (se perdió el asterisco del algoritmo).
- [x] **A9.** `Unidad 4/requirements.txt` está vacío (0 bytes). *(Completado con las dependencias reales de los imports: numpy, matplotlib, scikit-learn, tensorflow, opencv-python, transformers, torch — sin versiones fijadas porque no existía un entorno para hacer `freeze`. Nota: `torch` es necesario porque `GPT2LMHeadModel`/`tokenizer.encode(..., return_tensors="pt")` usa tensores de PyTorch, aunque el resto del notebook usa TensorFlow.)*

## A-bis. Ajustes adicionales solicitados (Unidad 1/1_Introducción.ipynb)

- [x] **A10.** Tablas con `<div style="width:...px">` no responsivas (se desbordan en pantallas angostas). Se quitaron los divs de ancho fijo: la tabla de definiciones quedó como tabla simple, y la lista de "Tipos de IA" + imagen se convirtió de tabla de 2 columnas a lista + imagen secuencial con `max-width:100%`.
- [x] **A11.** Columnas "Logo" en las tablas de Lenguajes/Frameworks/Entornos eliminadas (varios enlaces de imagen externos estaban rotos). De paso se corrigieron el enlace de R Project (apuntaba a una URL de Google Translate) y el de Google Colab (sin `https://`).
- [x] **A12.** Notas de instalación de `uv`: se añadió una sección específica sobre VS Code (o forks como Cursor) no detectando el kernel/entorno, incluyendo el caso de workspaces con múltiples `.venv` (abrir solo la subcarpeta relevante) y otras soluciones (instalar `ipykernel` en el entorno, reload window, seleccionar intérprete manualmente, registrar el kernel a mano, actualizar extensiones en forks).

## B. Unidad 1

- [ ] **B1.** "McCarthy, 1856" → debe ser 1956 (`1_Introducción.ipynb`).
- [ ] **B2.** Inconsistencia: `var = "!Hola Python!"` debería imprimir `"¡Hola Python!"` según el texto.
- [ ] **B3.** Enlace de Colab mal formado: `[colab.research.google.com](colab.research.google.com)` sin `https://`.
- [ ] **B4.** Typos: `</spam>` → `</span>` (`2_python_basics.ipynb`); "correpsondiente", "el el acceso" (`1_Introducción.ipynb`).
- [ ] **B5.** Outputs guardados con errores reales en `5_pydantic.ipynb` (celda 2) y `1_notebooks.ipynb` (celda 18).
- [ ] **B6.** `4_async_python.ipynb` muy escueto; no aclara que el `await` a nivel de celda es exclusivo de Jupyter.
- [ ] **B7.** Comentario menciona librería `openai` cuando el código usa `agents` (openai-agents SDK).

## C. Unidad 2

- [ ] **C1.** Rutas de imagen rotas con backslashes de Windows en `1_buscar-estados-ia.ipynb` (`..\Unidad 2\assets\...` → `assets/...`).
- [ ] **C2.** Typos varios: "correpsondiente", "compejidad", "uan rama", "anteirormente", "Algorimtos", "herística", "definira"/"el cúal", "valiendose", "argegar", "panatlla", "implmentación".
- [ ] **C3.** Rúbrica de `taller_u2.ipynb`: "Narrativa y Evidencias (Vibe Coding)" pesa 40%, más que Implementación (20%) y Algoritmos (15%) juntas — confirmar si es intencional.
- [ ] **C4.** (Menor) `app.py`: si el humano gana/empata, el panel "¿Cómo evaluó la IA su última jugada?" muestra el análisis del turno anterior.

## D. Unidad 3

- [ ] **D1.** `use_label_encoder=False` en `XGBClassifier` — parámetro obsoleto/eliminado.
- [ ] **D2.** `%pip install xgboost` / `%pip install pycaret` con output guardado `No module named pip`.
- [ ] **D3.** PyCaret + `numpy==2.3.4` fijado: riesgo de conflicto de dependencias; falta advertencia de entorno separado.
- [ ] **D4.** Leyenda cruzada en gráfico de California Housing ("Valor Real" / "Predicciones del Modelo" invertidas).
- [ ] **D5.** Tabla de ejemplo (Precio 100/150/200) vs. código (`y = [100000, 150000, 200000]`) — aclarar unidades.
- [ ] **D6.** `slides demo/5-data-preprocessing.ipynb`: ejemplo de estandarización usa la misma media/desviación para Altura y Peso (250/1), no realista.
- [ ] **D7.** `pLluviaNublado` en `3-teorema-bayes.ipynb` en realidad guarda `P(nublado|lluvia)` — nombre engañoso.
- [ ] **D8.** Web scraping de basketball-reference.com sin headers — puede dar 403 intermitente; ya existe `nba2019.csv` como alternativa.
- [ ] **D9.** Rutas absolutas personales filtradas en outputs guardados (incluye un `dir` completo del disco en `2-python-EDA.ipynb`).
- [ ] **D10.** Typos: "librearías", "valore reales", "Párametros", "Prepocesamiento", "porbabilidad". Tags rotos `<spam>` → `<span>` en `1_ML_implementation.ipynb`, `<span>` sin cerrar en `4-análisis-exploratorio-datos-EDA.ipynb`.
- [ ] **D11.** `KMeans` sin `n_init` explícito; `RandomForestClassifier()` sin `random_state` en un CV.

## E. Unidad 4

- [ ] **E1.** Sección "Transformers" vacía conceptualmente (solo instala `transformers` y corre GPT-2, sin explicar atención).
- [ ] **E2.** `IA_Moderna.ipynb` con poco texto explicativo del "por qué"; nunca se referencia con `computer-vision.ipynb`.
- [ ] **E3.** Comentario técnico incorrecto en `computer-vision.ipynb` (celda 60): el `-1` de `cv2.filter2D` es `ddepth`, no tiene relación con canales.
- [ ] **E4.** Error de traducción: "sumar" aparece como "resumir" en la explicación de convolución.
- [ ] **E5.** LSTM a nivel de carácter con corpus mínimo (~500 caracteres) genera texto roto sin nota de overfitting esperado.
- [ ] **E6.** Patrón de Keras desactualizado: `input_shape` en la primera capa (usar `Input(shape=...)`).
- [ ] **E7.** Imágenes embebidas como base64 en el markdown de `computer-vision.ipynb` (~20 celdas, infla el notebook a 4.6 MB).
- [ ] **E8.** Typos: "prediccíón", "HugginFace", "Concéptos", "tercer dimensión" (→ "tercera"), "coordendas".

## F. Unidad 5

- [ ] **F1.** `model="gemini-3.5-flash"` — ID de modelo que probablemente no existe; verificar el ID vigente.
- [ ] **F2.** Falta `langchain-classic` en el `!pip install` de la celda de dependencias, pero el código lo importa.
- [ ] **F3.** `llm_with_stop = llm.bind(stop=["Observation"])` se define pero nunca se usa.
- [ ] **F4.** Output guardado con error de Windows ("pip no se reconoce...") en la celda de instalación.
- [ ] **F5.** Typo en docstring: un `#` residual antes de `Returns:`.
