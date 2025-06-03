# Python Zombie Chess Engine with Custom Pieces and AI

A Python implementation of a custom chess‑variant featuring **Peons that mutate into Zombies, Flingers that hurl friendly pieces, and Cannons that bombard diagonals**. This game expands on traditional chess with unique mechanics and a powerful AI opponent driven by minimax and alpha-beta pruning.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Board File Format](#board-file-format)
4. [Running the Game](#running-the-game)
5. [Piece Guide](#piece-guide)
6. [Engine Architecture](#engine-architecture)
7. [Project Structure](#project-structure)
8. [Setup and Requirements](#setup-and-requirements)
9. [License](#license)

---

## Overview

This project implements a chess-like game engine in Python with:

* A fully-typed board model (`Board`)
* An extensible move generator (`MoveGenerator`)
* A minimax AI with alpha-beta pruning and iterative deepening (`AI`)
* Unique custom pieces and mechanics such as zombie contagion and flinger launches
* A text-based CLI for single-move or interactive play

The engine evaluates positions using a combination of material, positional tables (PSTs), king safety, mobility, pawn structure, capture analysis, and advancement.

---

## Quick Start

```bash
# 1 - Run the AI once to get its best move
python main.py
```

> Python ≥ 3.11 is required; NumPy is the only third-party dependency.

---

## Board File Format

Plain-text format with 4 parameters and a dictionary-style piece list:

```
w 0 60000 0
{
  a2: 'wP',
  e2: 'wZ',
  e7: 'bZ',
  ...
}
0
0
0
```

* **Turn** – `w` or `b`
* **Used Time / Total Time** – in milliseconds
* **Move Number** – full-move count (0-indexed)

---

## Piece Guide

### Standard Pieces

| Symbol | Piece  | Movement                    |
| ------ | ------ | --------------------------- |
| K      | King   | One square in any direction |
| Q      | Queen  | Orthogonal and diagonal     |
| R      | Rook   | Horizontal and vertical     |
| B      | Bishop | Diagonal only               |
| N      | Knight | L-shaped jumps              |

### Custom Pieces

| Symbol | Piece   | Description                                                                              |
| ------ | ------- | ---------------------------------------------------------------------------------------- |
| P      | Peon    | Moves like a pawn. Promotes to Zombie at final rank.                                     |
| Z      | Zombie  | Moves like a king. After moving, infects orthogonally-adjacent enemy Peons into Zombies. |
| F      | Flinger | Can move or fling adjacent friendly pieces. Landing on enemy destroys both pieces.       |
| C      | Cannon  | Moves diagonally. Can fire to destroy all pieces on a diagonal without moving.           |

*Contagion, slinging, and cannonball effects are automatically handled by the engine logic.*

---

## Engine Architecture

The AI system in this project is a key highlight—designed to provide competitive gameplay through strategic foresight, heuristic evaluation, and time-efficient decision making.

### Evaluation Function

At the core of the AI is a custom evaluation function that scores the board based on a wide array of factors. Each factor is weighted to influence the engine's positional judgment and long-term planning. Key components include:
The AI uses a deep scoring function combining:

* **Material balance** (piece values)
* **Piece-square tables (PSTs)** for positional scoring
* **King safety** (pawn shields, threats, open files)
* **Mobility** (move counts, center control)
* **Pawn structure** (isolated, doubled, passed pawns)
* **Capture history**
* **Pawn/Zombie advancement bonuses**

### Search

The AI uses a Minimax algorithm with Alpha-Beta pruning to explore game states and choose optimal moves. It supports the following enhancements:

* **Minimax with alpha-beta pruning**
* **Iterative deepening** with dynamic depth control based on remaining time
* **Move ordering** (captures, checks, etc.)
* **Opening book** for predefined early moves
* **Time-aware depth control** – The AI dynamically adjusts its search depth based on the remaining time. For instance, with ample time it searches deeper, but when under pressure, it falls back to shallower but faster evaluations.
* **Fail-soft return** – The AI returns the best result found within the allowed time window even if it doesn't reach the full target depth.
* **Self-checkmate avoidance** – The AI deprioritizes any move that would lead to its own king's capture, even if the score otherwise seems high.
* **Custom move sorting** – Before exploring child positions, the AI prioritizes moves based on tactical potential (captures, checks, cannon blasts, sling hits, etc.), improving pruning efficiency.

Together, these features allow the AI to respond quickly in early games, make strong mid-game decisions, and survive time scrambles in endgames.

---

## Project Structure

```
.
├── main.py            # One-off AI move
├── interactive.py     # Turn-based game loop (human vs AI)
├── Board.py           # Game board and mechanics
├── AI.py              # Minimax AI with evaluation
├── MoveGenerator.py   # Handles move application, flingers, cannons, contagion
├── utils.py           # File parsers and helpers
├── pieces/            # Each piece's behavior
│   ├── base.py
│   ├── king.py
│   ├── zombie.py
│   ├── peon.py
│   ├── flinger.py
│   ├── cannon.py
│   └── ...
└── board              # Sample board input file
```

---

## Setup and Requirements

### Prerequisites

* Python 3.11+
* NumPy

### Installation

```bash
pip install numpy
```

### Preparing the Board File

```
w
0
60000
0
wKe1,wPa2,bKe8,bZf7
```

* Format: `<turn>`, `<used time>`, `<total time>`, `<move count>`, `<piece list>`

---

## License

This project is released under the MIT License. See `LICENSE` for details.
