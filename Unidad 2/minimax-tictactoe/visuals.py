"""Utilidades de dibujo para la interfaz de Streamlit: el árbol de MinMax
y el tablero en miniatura. Separado de app.py para que la lógica de la
interfaz principal sea más fácil de seguir.
"""
import base64
import io
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import minimax as mm


def fmt_inf(x):
    if x == math.inf:
        return "+∞"
    if x == -math.inf:
        return "-∞"
    return str(x)


def _collect(node, out):
    out[node.id] = node
    for c in node.children:
        _collect(c, out)


DEPTH_GAP = 1.4  # separación vertical entre niveles del árbol


def _assign_x(node, positions, counter, depth=0):
    if not node.children:
        x = counter[0]
        counter[0] += 1
    else:
        xs = [_assign_x(c, positions, counter, depth + 1) for c in node.children]
        x = sum(xs) / len(xs)
    positions[node.id] = (x, -depth * DEPTH_GAP)
    return x


def index_events(events):
    """Índice: id de nodo -> paso en el que ocurrió su 'enter'/'exit'/'prune'."""
    enter_idx, exit_idx, prune_idx = {}, {}, {}
    for i, ev in enumerate(events):
        kind = ev[0]
        node = ev[1]
        if kind == "enter":
            enter_idx.setdefault(node.id, i)
        elif kind == "exit":
            exit_idx[node.id] = i
        elif kind == "prune":
            prune_idx[node.id] = i
    return enter_idx, exit_idx, prune_idx


def full_reveal_sets(root):
    """Todo el árbol ya construido y "revelado" (para vistas estáticas)."""
    all_nodes = {}
    _collect(root, all_nodes)
    pruned = {nid for nid, n in all_nodes.items() if n.pruned_moves}
    ids = set(all_nodes.keys())
    return ids, ids, pruned


UNIT = 0.62      # pulgadas por unidad de dato, en el caso normal
MAX_HEIGHT_IN = 9.0  # tope de alto; el ancho se deriva con la MISMA escala


def draw_tree(root, revealed_ids, exited_ids, pruned_ids, current_id=None):
    positions = {}
    _assign_x(root, positions, [0])
    all_nodes = {}
    _collect(root, all_nodes)

    max_x = max((x for x, _ in positions.values()), default=0)
    max_depth = max((-y for _, y in positions.values()), default=0)  # ya en unidades de DEPTH_GAP

    data_w = max_x + 2.2
    data_h = max_depth + 2.8
    # Una sola escala para ancho y alto: así la figura pedida a matplotlib
    # ya tiene la proporción real de los datos y set_aspect("equal") no
    # tiene que recortar/rellenar nada (lo que antes deformaba el resultado
    # final tras el recorte "tight" que hace Streamlit al guardar la imagen).
    # Los pisos mínimos se aplican subiendo la MISMA escala, nunca ancho y
    # alto por separado, para no reintroducir el desajuste de proporción.
    scale = min(UNIT, MAX_HEIGHT_IN / data_h)
    scale = max(scale, 2.6 / data_w, 2.2 / data_h)
    fig_w = data_w * scale
    fig_h = data_h * scale

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    # aristas reales
    for node in all_nodes.values():
        if node.id not in revealed_ids:
            continue
        x1, y1 = positions[node.id]
        for child in node.children:
            if child.id not in revealed_ids:
                continue
            x2, y2 = positions[child.id]
            ax.plot([x1, x2], [y1 - 0.15, y2 + 0.15], color="#9aa5b1",
                     linewidth=1.2, zorder=1)
            # etiqueta cerca del hijo, lejos de la etiqueta MAX/MIN del padre
            mx, my = x1 + 0.72 * (x2 - x1), y1 + 0.72 * (y2 - y1)
            ax.text(mx, my, str(child.move + 1), fontsize=8, color="#5a6674",
                     ha="center", va="center",
                     bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec="#9aa5b1", lw=0.6),
                     zorder=4)

        # ramas podadas: se dibujan como líneas cortadas fantasma, a la
        # derecha de los hijos reales para no encimarse con ellos
        if node.id in pruned_ids and node.pruned_moves:
            real_children_x = [positions[c.id][0] for c in node.children if c.id in revealed_ids]
            start_x = max(real_children_x) if real_children_x else x1
            for k, mv in enumerate(node.pruned_moves):
                gx = start_x + 0.6 * (k + 1)
                gy = y1 - DEPTH_GAP
                ax.plot([x1, gx], [y1 - 0.15, gy + 0.2], color="#d98c8c",
                         linewidth=1.1, linestyle="--", zorder=1)
                ax.text(gx, gy, f"✂ {mv + 1}", fontsize=8, color="#c0392b",
                         ha="center", va="center", zorder=4)

    # nodos
    for node in all_nodes.values():
        if node.id not in revealed_ids:
            continue
        x, y = positions[node.id]
        known = node.id in exited_ids
        if known and node.is_terminal_node:
            face, edge = {
                "win_ai": ("#d4edda", "#28a745"),
                "win_human": ("#f8d7da", "#dc3545"),
                "draw": ("#e2e3e5", "#6c757d"),
            }[node.terminal_reason]
        else:
            face = "#eaf1fb" if node.player == "MAX" else "#fdf1e7"
            edge = "#2f6fb0" if node.player == "MAX" else "#c07a2b"
        lw = 2.8 if node.id == current_id else 1.2
        if node.id == current_id:
            edge = "#111111"
        circle = plt.Circle((x, y), 0.34, facecolor=face, edgecolor=edge,
                             linewidth=lw, zorder=2)
        ax.add_patch(circle)
        label = str(node.value) if known else "?"
        ax.text(x, y, label, ha="center", va="center", fontsize=9,
                 fontweight="bold", zorder=3)
        if not (known and node.is_terminal_node):
            ax.text(x, y - 0.44, node.player, ha="center", va="center",
                     fontsize=7, color="#666666", zorder=3)

    ax.set_xlim(-1, max_x + 1)
    ax.set_ylim(-max_depth - 1.6, 1)
    fig.tight_layout()
    return fig


def fig_to_scrollable_html(fig, display_height_px=380):
    """Convierte la figura a <img> con una altura fija en CSS, dentro de un
    contenedor con scroll horizontal. A diferencia de st.pyplot (que ajusta
    la imagen al ancho de la columna y por lo tanto la aplasta cuando el
    árbol es muy ancho), esto mantiene siempre el mismo tamaño visual por
    nodo y dado que solo se fija la altura, el navegador nunca deforma la
    proporción: el ancho se calcula solo automáticamente.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    # max-width:none es imprescindible: Streamlit define "img { max-width:
    # 100% }" globalmente, y combinado con una altura fija eso deforma la
    # imagen (el navegador no puede respetar la proporción real si el ancho
    # queda topado al contenedor pero el alto se fuerza en píxeles).
    return (
        '<div style="overflow-x:auto; overflow-y:hidden; padding:6px 0;">'
        f'<img src="data:image/png;base64,{b64}" '
        f'style="height:{display_height_px}px; width:auto; max-width:none; display:block;">'
        "</div>"
    )


def render_board_html(board, highlight=None):
    symbols = {"X": "❌", "O": "⭕", mm.EMPTY: ""}
    cells = []
    for i, v in enumerate(board):
        bg = "#fff3cd" if i == highlight else "#ffffff"
        cells.append(
            f'<div style="width:42px;height:42px;display:flex;align-items:center;'
            f'justify-content:center;border:1px solid #ccc;background:{bg};'
            f'font-size:18px;">{symbols[v]}</div>'
        )
    rows = "".join(
        f'<div style="display:flex;">{"".join(cells[r * 3:(r + 1) * 3])}</div>'
        for r in range(3)
    )
    return f'<div style="display:inline-block;">{rows}</div>'
