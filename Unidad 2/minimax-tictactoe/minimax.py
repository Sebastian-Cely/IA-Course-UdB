"""Lógica del Tres en Raya y del algoritmo MinMax con poda alfa-beta.

Este módulo no depende de Streamlit: contiene únicamente las reglas del
juego y el algoritmo, para que se pueda leer como "el algoritmo" separado
de la interfaz gráfica.
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from typing import Optional

EMPTY = " "

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # filas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columnas
    (0, 4, 8), (2, 4, 6),             # diagonales
]


def new_board():
    return [EMPTY] * 9


def check_winner(board):
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def available_moves(board):
    return [i for i, v in enumerate(board) if v == EMPTY]


def infer_next_mover(board):
    """Asume que X siempre mueve primero y deduce a quién le toca ahora."""
    return "X" if board.count("X") == board.count("O") else "O"


def score_terminal(board, depth, ai_symbol, human_symbol):
    winner = check_winner(board)
    if winner == ai_symbol:
        return 10 - depth
    if winner == human_symbol:
        return depth - 10
    return 0


@dataclass
class Node:
    id: int
    board: tuple
    player: str  # "MAX" o "MIN": a quién le toca mover EN este nodo
    depth: int
    move: Optional[int] = None       # casilla jugada para llegar a este nodo
    moved_by: Optional[str] = None   # símbolo que jugó esa casilla
    alpha_in: float = -math.inf
    beta_in: float = math.inf
    alpha_out: float = -math.inf
    beta_out: float = math.inf
    value: Optional[int] = None
    is_terminal_node: bool = False
    terminal_reason: Optional[str] = None
    children: list = field(default_factory=list)
    pruned_moves: list = field(default_factory=list)  # casillas no exploradas


_id_counter = itertools.count()


def _new_id():
    return next(_id_counter)


def _reset_ids():
    global _id_counter
    _id_counter = itertools.count()


def minimax_trace(board, ai_symbol, human_symbol, maximizing, depth=0,
                   alpha=-math.inf, beta=math.inf, use_ab=True,
                   move=None, moved_by=None):
    """Generador que recorre el árbol MinMax en preorden, emitiendo eventos
    ('enter' | 'child_done' | 'prune' | 'exit') exactamente en el orden en
    que ocurrirían con la pila de llamadas recursivas real.

    Al terminar, devuelve (a través de StopIteration.value / `yield from`)
    el nodo raíz con todo su árbol de hijos ya construido.
    """
    node = Node(
        id=_new_id(), board=tuple(board), player="MAX" if maximizing else "MIN",
        depth=depth, move=move, moved_by=moved_by,
        alpha_in=alpha, beta_in=beta, alpha_out=alpha, beta_out=beta,
    )
    yield ("enter", node)

    winner = check_winner(board)
    if winner is not None or is_full(board):
        node.is_terminal_node = True
        node.terminal_reason = (
            "win_ai" if winner == ai_symbol else
            "win_human" if winner == human_symbol else
            "draw"
        )
        node.value = score_terminal(board, depth, ai_symbol, human_symbol)
        yield ("exit", node)
        return node

    moves = available_moves(board)
    symbol = ai_symbol if maximizing else human_symbol
    best = -math.inf if maximizing else math.inf

    for i, m in enumerate(moves):
        child_board = list(board)
        child_board[m] = symbol
        child = yield from minimax_trace(
            child_board, ai_symbol, human_symbol, not maximizing, depth + 1,
            alpha, beta, use_ab, move=m, moved_by=symbol,
        )
        node.children.append(child)

        if maximizing:
            best = max(best, child.value)
            alpha = max(alpha, best)
        else:
            best = min(best, child.value)
            beta = min(beta, best)

        node.alpha_out, node.beta_out = alpha, beta
        yield ("child_done", node, child, alpha, beta)

        if use_ab and beta <= alpha:
            skipped = moves[i + 1:]
            if skipped:
                node.pruned_moves = skipped
                yield ("prune", node, skipped, alpha, beta)
            break

    node.value = best
    yield ("exit", node)
    return node


def build_tree(board, ai_symbol, human_symbol, maximizing, use_ab=True):
    """Ejecuta minimax_trace por completo y devuelve (raiz, lista_eventos)."""
    _reset_ids()
    events = []
    gen = minimax_trace(board, ai_symbol, human_symbol, maximizing, use_ab=use_ab)
    root = None
    try:
        while True:
            events.append(next(gen))
    except StopIteration as stop:
        root = stop.value
    return root, events


def count_nodes(node):
    return 1 + sum(count_nodes(c) for c in node.children)


def best_move(board, ai_symbol, human_symbol, use_ab=True):
    """La IA (símbolo ai_symbol) siempre se evalúa como jugador MAX."""
    root, events = build_tree(board, ai_symbol, human_symbol, True, use_ab=use_ab)
    if not root.children:
        return None, root, events
    best_child = max(root.children, key=lambda c: c.value)
    return best_child.move, root, events
