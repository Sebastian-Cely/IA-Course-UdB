import random
import time

import pandas as pd
import streamlit as st

import minimax as mm
import visuals
from visuals import fmt_inf, render_board_html

st.set_page_config(page_title="MinMax · Tres en Raya", page_icon="❌⭕", layout="wide")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        height: 60px;
        font-size: 26px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DIFICULTADES = [
    "Aleatoria total",
    "Fácil (subóptima)",
    "Perfecta (MinMax completo)",
]

ESCENARIOS = {
    "1 · Muy sencillo (2 casillas libres)": [
        "X", "O", "X", "O", "O", "X", mm.EMPTY, "X", mm.EMPTY,
    ],
    "2 · Varias jugadas ganadoras (3 casillas libres)": [
        "X", "O", "X", "O", "X", "O", mm.EMPTY, mm.EMPTY, mm.EMPTY,
    ],
    "3 · Hay que bloquear (5 casillas libres)": [
        "X", mm.EMPTY, mm.EMPTY, "O", "O", mm.EMPTY, "X", mm.EMPTY, mm.EMPTY,
    ],
}


# ---------------------------------------------------------------------------
# Utilidades compartidas
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def cached_build_tree(board_tuple, ai_symbol, human_symbol, use_ab):
    root, events = mm.build_tree(list(board_tuple), ai_symbol, human_symbol, True, use_ab=use_ab)
    return root, events


@st.cache_data(show_spinner=False)
def cached_count(board_tuple, ai_symbol, human_symbol, use_ab):
    root, _ = mm.build_tree(list(board_tuple), ai_symbol, human_symbol, True, use_ab=use_ab)
    return mm.count_nodes(root)


def get_ai_move(board, ai_symbol, human_symbol, dificultad):
    moves = mm.available_moves(board)
    if not moves:
        return None, None
    if dificultad == "Aleatoria total":
        return random.choice(moves), None

    # La poda alfa-beta siempre da el mismo resultado que MinMax completo,
    # solo que explorando menos nodos, así que se usa para toda partida real.
    root, _ = cached_build_tree(tuple(board), ai_symbol, human_symbol, use_ab=True)
    if not root.children:
        return None, root

    best_val = max(c.value for c in root.children)
    if dificultad == "Fácil (subóptima)":
        candidatos = [c for c in root.children if c.value >= best_val - 2]
    else:
        candidatos = [c for c in root.children if c.value == best_val]
    chosen = random.choice(candidatos)
    return chosen.move, root


def random_scenario(filled_count, max_tries=300):
    for _ in range(max_tries):
        board = mm.new_board()
        cells = random.sample(range(9), filled_count)
        for idx, cell in enumerate(cells):
            board[cell] = "X" if idx % 2 == 0 else "O"
        if mm.check_winner(board) is None:
            return board
    return mm.new_board()


def describe_event(ev, ai_symbol, human_symbol):
    kind = ev[0]
    node = ev[1]
    quien = f"la IA (MAX, juega {ai_symbol})" if node.player == "MAX" else f"el rival (MIN, juega {human_symbol})"
    origen = "el tablero inicial de este escenario" if node.move is None else f"la casilla {node.move + 1}"

    if kind == "enter":
        return (f"**➡️ Entramos a un nuevo nodo (profundidad {node.depth}).** "
                f"Aquí le toca mover a {quien}. Se llegó a este tablero jugando en {origen}.")
    if kind == "child_done":
        child = ev[2]
        alpha, beta = ev[3], ev[4]
        return (f"**↩️ Volvemos de explorar la jugada en la casilla {child.move + 1}**, que valió **{child.value}**. "
                f"{quien.capitalize()} actualiza su mejor valor conocido. "
                f"Ventana actual → α = {fmt_inf(alpha)}, β = {fmt_inf(beta)}.")
    if kind == "prune":
        skipped = ev[2]
        alpha, beta = ev[3], ev[4]
        casillas = ", ".join(str(c + 1) for c in skipped)
        return (f"**✂️ ¡Poda alfa-beta!** Como β ({fmt_inf(beta)}) ≤ α ({fmt_inf(alpha)}), ya sabemos que "
                f"{quien} nunca dejaría llegar el juego a este nodo. Nos ahorramos explorar la(s) casilla(s) {casillas}.")
    if kind == "exit":
        if node.is_terminal_node:
            motivo = {"win_ai": "🏆 gana la IA", "win_human": "🙁 gana el rival", "draw": "🤝 empate"}[node.terminal_reason]
            return f"**🍃 Nodo hoja.** Resultado del tablero: {motivo}. Valor = **{node.value}**."
        return (f"**⬅️ Terminamos de evaluar este nodo.** Su valor final es **{node.value}**, "
                f"que se le devuelve a su nodo padre.")
    return ""


# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------

st.title("❌⭕ Tres en Raya con MinMax")
st.caption("Laboratorio interactivo para entender el algoritmo MinMax y la poda alfa-beta — Inteligencia Artificial, Unidad 2.")

tab_jugar, tab_teoria, tab_explora, tab_poda = st.tabs([
    "🎮 Jugar contra la IA",
    "📖 ¿Qué es MinMax?",
    "🔍 Explora el árbol paso a paso",
    "⚡ Poda Alfa-Beta",
])


# ---------------------------------------------------------------------------
# Tab 1 · Jugar
# ---------------------------------------------------------------------------

def reset_game(human_symbol, dificultad):
    st.session_state.board = mm.new_board()
    st.session_state.human_symbol = human_symbol
    st.session_state.ai_symbol = "O" if human_symbol == "X" else "X"
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.last_root = None
    if st.session_state.ai_symbol == "X":
        move, root = get_ai_move(st.session_state.board, st.session_state.ai_symbol,
                                  st.session_state.human_symbol, dificultad)
        if move is not None:
            st.session_state.board[move] = st.session_state.ai_symbol
        st.session_state.last_root = root


def finish_game(winner):
    st.session_state.game_over = True
    st.session_state.winner = winner


def handle_human_click(i, dificultad):
    board = st.session_state.board
    if st.session_state.game_over or board[i] != mm.EMPTY:
        return
    board[i] = st.session_state.human_symbol
    winner = mm.check_winner(board)
    if winner or mm.is_full(board):
        finish_game(winner)
        return
    move, root = get_ai_move(board, st.session_state.ai_symbol,
                              st.session_state.human_symbol, dificultad)
    st.session_state.last_root = root
    if move is not None:
        board[move] = st.session_state.ai_symbol
    winner = mm.check_winner(board)
    if winner or mm.is_full(board):
        finish_game(winner)


with tab_jugar:
    left, right = st.columns([1, 1])

    with left:
        st.subheader("⚙️ Configuración")
        simbolo = st.radio("Tu símbolo", ["X", "O"], horizontal=True,
                            help="X siempre mueve primero, como en las reglas clásicas.")
        dificultad = st.select_slider("Dificultad de la IA", options=DIFICULTADES,
                                       value="Perfecta (MinMax completo)")
        mostrar_valores = st.checkbox("Mostrar cómo evaluó la IA sus jugadas", value=True)
        reiniciar_click = st.button("🔄 Reiniciar partida")

        if "_last_symbol" not in st.session_state or st.session_state._last_symbol != simbolo or reiniciar_click:
            st.session_state._last_symbol = simbolo
            reset_game(simbolo, dificultad)

        st.divider()
        if st.session_state.game_over:
            if st.session_state.winner == st.session_state.human_symbol:
                st.success("🎉 ¡Ganaste! Venciste al MinMax.")
            elif st.session_state.winner == st.session_state.ai_symbol:
                st.error("🤖 La IA (MinMax) ganó esta vez.")
            else:
                st.info("🤝 Empate. Si la IA juega perfecto, ¡esto es lo máximo que puedes lograr!")
        else:
            st.write("🧑 Es tu turno — haz clic en una casilla.")

    with right:
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                i = r * 3 + c
                val = st.session_state.board[i]
                label = {"X": "❌", "O": "⭕", mm.EMPTY: " "}[val]
                disabled = val != mm.EMPTY or st.session_state.game_over
                if cols[c].button(label, key=f"cell_{i}", disabled=disabled, use_container_width=True):
                    handle_human_click(i, dificultad)
                    st.rerun()

    if mostrar_valores and st.session_state.last_root and st.session_state.last_root.children:
        st.divider()
        st.subheader("🧠 ¿Cómo evaluó la IA su última jugada?")
        root = st.session_state.last_root
        data = {f"Casilla {c.move + 1}": c.value for c in sorted(root.children, key=lambda c: c.move)}
        st.bar_chart(pd.Series(data), height=220)
        elegido = max(root.children, key=lambda c: c.value)
        st.caption(
            f"La IA (MAX) eligió la casilla {elegido.move + 1} porque, de todas sus opciones, "
            f"es la que le garantiza el mejor resultado posible (valor {elegido.value}) suponiendo "
            f"que el rival también juega lo mejor que puede."
        )


# ---------------------------------------------------------------------------
# Tab 2 · Teoría
# ---------------------------------------------------------------------------

with tab_teoria:
    st.header("📖 ¿Qué es el algoritmo MinMax?")

    st.markdown(
        """
MinMax es el algoritmo clásico para tomar decisiones en **juegos de dos
jugadores, de suma cero y con información perfecta** (ambos jugadores ven
todo el tablero, no hay azar y lo que gana uno lo pierde el otro). El Tres
en Raya cumple exactamente esas condiciones, por eso es el ejemplo favorito
para enseñarlo.

### El árbol de juego
Cada posible tablero es un **nodo**; cada jugada legal es una **arista**
hacia un nuevo nodo. Empezando desde el tablero actual, ese árbol contiene
*todas* las partidas posibles desde ese punto en adelante.

### Dos jugadores, dos objetivos opuestos
- **MAX** (la IA, en esta app) quiere el valor **más alto** posible.
- **MIN** (el rival) quiere el valor **más bajo** posible.

Cada nodo hoja (tablero terminado) recibe un valor de utilidad:

| Resultado | Valor |
|---|---|
| Gana MAX | `10 − profundidad` |
| Gana MIN | `profundidad − 10` |
| Empate | `0` |

Restar la profundidad hace que la IA **prefiera ganar rápido** y, si va a
perder, **prefiera perder tarde** (quizás el rival se equivoque en el camino).

### Propagación hacia atrás ("backward induction")
El algoritmo no puede saber el valor de un nodo hasta conocer el de **todos
sus hijos**. Por eso primero baja hasta las hojas y luego sube, calculando
en cada nodo el máximo (si es turno de MAX) o el mínimo (si es turno de MIN)
de los valores de sus hijos.
        """
    )

    st.code(
        """function minimax(tablero, profundidad, es_turno_de_max):
    si tablero es terminal:
        return utilidad(tablero, profundidad)

    si es_turno_de_max:
        mejor = -infinito
        para cada jugada posible:
            valor = minimax(resultado(tablero, jugada), profundidad + 1, False)
            mejor = max(mejor, valor)
        return mejor
    si_no:
        mejor = +infinito
        para cada jugada posible:
            valor = minimax(resultado(tablero, jugada), profundidad + 1, True)
            mejor = min(mejor, valor)
        return mejor""",
        language="text",
    )

    st.markdown(
        """
### ¿Por qué en Tres en Raya sí y en ajedrez no?
Desde el tablero vacío, el árbol completo de Tres en Raya tiene menos de un
millón de nodos: un computador lo recorre en segundos. El árbol del ajedrez
tiene más nodos que átomos estimados en el universo observable — de ahí que
se necesiten técnicas adicionales como la **poda alfa-beta** (pestaña
siguiente) para hacer factible la búsqueda.

### Ejemplo mínimo, completamente resuelto
Este es el escenario **"Muy sencillo"** (solo 2 casillas libres) evaluado
por completo, para ver de un vistazo cómo los valores de las hojas suben
hacia la raíz:
        """
    )

    _board_ej = ESCENARIOS["1 · Muy sencillo (2 casillas libres)"]
    _ai_ej = mm.infer_next_mover(_board_ej)
    _human_ej = "O" if _ai_ej == "X" else "X"
    _root_ej, _ = cached_build_tree(tuple(_board_ej), _ai_ej, _human_ej, True)
    _revealed, _exited, _pruned = visuals.full_reveal_sets(_root_ej)
    _fig_ej = visuals.draw_tree(_root_ej, _revealed, _exited, _pruned)
    st.markdown(visuals.fig_to_scrollable_html(_fig_ej, display_height_px=300), unsafe_allow_html=True)
    st.caption(
        "Los círculos azules son turnos de MAX (la IA), los naranjas son turnos de MIN (el rival). "
        "El número en cada arista es la casilla jugada."
    )


# ---------------------------------------------------------------------------
# Tab 3 · Explora paso a paso
# ---------------------------------------------------------------------------

def set_step(value, n_events):
    st.session_state.step = max(0, min(n_events - 1, value))


with tab_explora:
    st.header("🔍 Explora el árbol de decisión, paso a paso")
    st.write(
        "Elige un escenario y avanza evento por evento, exactamente como lo haría "
        "la recursión de MinMax en la memoria del computador."
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        escenario_nombre = st.selectbox("Escenario", list(ESCENARIOS.keys()), key="escenario_sel")
    with c2:
        usar_poda = st.checkbox("Usar poda alfa-beta", value=True, key="poda_explora")

    board = ESCENARIOS[escenario_nombre]
    ai_symbol = mm.infer_next_mover(board)
    human_symbol = "O" if ai_symbol == "X" else "X"

    st.markdown(f"Tablero de partida (le toca mover a **MAX**, símbolo **{ai_symbol}**):")
    st.markdown(render_board_html(board), unsafe_allow_html=True)

    cache_key = (escenario_nombre, usar_poda)
    if st.session_state.get("_explora_key") != cache_key or "step" not in st.session_state:
        root, events = cached_build_tree(tuple(board), ai_symbol, human_symbol, usar_poda)
        st.session_state._explora_key = cache_key
        st.session_state._explora_root = root
        st.session_state._explora_events = events
        st.session_state.step = 0

    root = st.session_state._explora_root
    events = st.session_state._explora_events
    n_events = len(events)

    # El avance del auto-play se aplica ANTES de crear el slider "step":
    # Streamlit no permite mutar st.session_state.step después de que ese
    # widget ya fue instanciado en esta misma ejecución.
    if st.session_state.get("_autoplay_tick"):
        st.session_state._autoplay_tick = False
        st.session_state.step = min(n_events - 1, st.session_state.step + 1)

    nav1, nav2, nav3, nav4, nav5 = st.columns(5)
    nav1.button("⏮ Inicio", on_click=set_step, args=(0, n_events))
    nav2.button("◀ Anterior", on_click=set_step, args=(st.session_state.step - 1, n_events))
    nav3.button("Siguiente ▶", on_click=set_step, args=(st.session_state.step + 1, n_events))
    nav4.button("Final ⏭", on_click=set_step, args=(n_events - 1, n_events))
    autoplay = nav5.checkbox("▶️ Auto")

    st.slider("Paso", 0, n_events - 1, key="step")
    step = st.session_state.step
    ev = events[step]
    node = ev[1]

    enter_idx, exit_idx, prune_idx = visuals.index_events(events)
    revealed = {nid for nid, i in enter_idx.items() if i <= step}
    exited = {nid for nid, i in exit_idx.items() if i <= step}
    pruned_now = {nid for nid, i in prune_idx.items() if i <= step}

    st.progress((step + 1) / n_events, text=f"Paso {step + 1} de {n_events}")
    st.markdown(describe_event(ev, ai_symbol, human_symbol))

    col_tree, col_detail = st.columns([2, 1])
    with col_tree:
        fig = visuals.draw_tree(root, revealed, exited, pruned_now, current_id=node.id)
        st.markdown(visuals.fig_to_scrollable_html(fig, display_height_px=380), unsafe_allow_html=True)
    with col_detail:
        st.markdown("**Nodo actual**")
        st.write(f"Profundidad: {node.depth}")
        st.write(f"Turno: {'IA (MAX)' if node.player == 'MAX' else 'Rival (MIN)'}")
        st.write(f"α / β: {fmt_inf(node.alpha_out)} / {fmt_inf(node.beta_out)}")
        st.markdown(render_board_html(node.board, node.move), unsafe_allow_html=True)

    if step == n_events - 1 and root.children:
        mejor = max(root.children, key=lambda c: c.value)
        st.success(
            f"✅ Conclusión: MinMax recomienda jugar en la casilla {mejor.move + 1} "
            f"(valor {mejor.value}), la mejor opción garantizada para MAX."
        )

# ---------------------------------------------------------------------------
# Tab 4 · Poda alfa-beta
# ---------------------------------------------------------------------------

with tab_poda:
    st.header("⚡ ¿Cuánto ahorra la poda alfa-beta?")

    st.markdown(
        """
La poda alfa-beta no cambia la decisión de MinMax — llega **exactamente**
a la misma jugada — pero evita explorar ramas que ya sabemos que nunca
ocurrirían en juego óptimo.

- **α (alfa):** el mejor valor que MAX puede garantizar hasta ahora.
- **β (beta):** el mejor valor que MIN puede garantizar hasta ahora.
- **Se poda** un nodo en cuanto `β ≤ α`: significa que el jugador de más
  arriba en el árbol ya tiene una alternativa mejor y jamás elegiría el
  camino que llevaría a este nodo, sin importar lo que se calcule debajo.
        """
    )
    st.code(
        """función minimax_ab(tablero, profundidad, es_turno_de_max, alfa, beta):
    si tablero es terminal:
        return utilidad(tablero, profundidad)

    si es_turno_de_max:
        mejor = -infinito
        para cada jugada posible:
            valor = minimax_ab(resultado(tablero, jugada), profundidad+1, False, alfa, beta)
            mejor = max(mejor, valor)
            alfa = max(alfa, mejor)
            si beta <= alfa:
                romper   # poda: MIN nunca dejaría llegar el juego aquí
        return mejor
    # (el caso MIN es simétrico, actualizando beta)""",
        language="text",
    )

    st.subheader("Compara nodos explorados: con poda vs. sin poda")
    modo = st.radio("Tablero a analizar", ["Usar un escenario de ejemplo", "Generar uno aleatorio"], horizontal=True)

    if modo == "Usar un escenario de ejemplo":
        nombre = st.selectbox("Escenario", list(ESCENARIOS.keys()), key="escenario_poda")
        board = ESCENARIOS[nombre]
    else:
        n_vacias = st.slider("Casillas vacías en el tablero aleatorio", 2, 6, 4, key="vacias_poda")
        if st.button("🎲 Generar tablero aleatorio") or "_board_poda" not in st.session_state:
            st.session_state._board_poda = random_scenario(9 - n_vacias)
        board = st.session_state._board_poda

    st.markdown(render_board_html(board), unsafe_allow_html=True)
    ai_symbol = mm.infer_next_mover(board)
    human_symbol = "O" if ai_symbol == "X" else "X"
    n_vacias_real = board.count(mm.EMPTY)

    if n_vacias_real > 6:
        st.warning(
            "Este tablero tiene bastantes casillas libres: calcular sin poda puede tardar varios "
            "segundos porque el árbol crece factorialmente. ¡Esa lentitud es justamente la lección!"
        )

    if st.button("▶️ Comparar", type="primary"):
        with st.spinner("Explorando el árbol completo (sin poda)..."):
            t0 = time.perf_counter()
            nodos_sin = cached_count(tuple(board), ai_symbol, human_symbol, False)
            t_sin = time.perf_counter() - t0
        with st.spinner("Explorando con poda alfa-beta..."):
            t0 = time.perf_counter()
            nodos_con = cached_count(tuple(board), ai_symbol, human_symbol, True)
            t_con = time.perf_counter() - t0

        c1, c2, c3 = st.columns(3)
        c1.metric("Nodos sin poda", f"{nodos_sin:,}")
        c2.metric("Nodos con poda", f"{nodos_con:,}", delta=f"-{nodos_sin - nodos_con:,}")
        ahorro = 0 if nodos_sin == 0 else 100 * (1 - nodos_con / nodos_sin)
        c3.metric("Nodos ahorrados", f"{ahorro:.1f}%")
        st.bar_chart(pd.Series({"Sin poda": nodos_sin, "Con poda": nodos_con}))
        st.caption(f"Tiempo sin poda: {t_sin * 1000:.1f} ms · Tiempo con poda: {t_con * 1000:.1f} ms "
                   "(el tiempo absoluto depende del computador; lo importante es la diferencia relativa).")


# ---------------------------------------------------------------------------
# Auto-play de la pestaña "Explora": se dispara al final de TODO el script,
# después de que las demás pestañas (incluida "Poda Alfa-Beta") ya se
# dibujaron por completo. Si el rerun ocurriera antes, esas pestañas se
# quedarían sin renderizar en cada ciclo del auto-play.
# ---------------------------------------------------------------------------

if autoplay and step < n_events - 1:
    time.sleep(0.5)
    st.session_state._autoplay_tick = True
    st.rerun()
