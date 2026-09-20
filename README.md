# Murdoku Solver

An SMT-based constraint solver for [Murdoku](https://murdoku.com/play), the popular logic puzzle game where **Sudoku meets murder mystery** (created by Manuel Garand).

![Murdoku](img/murdoku.png)

---

## What is Murdoku?

In **Murdoku**, you are a detective investigating a crime scene laid out on a 2D grid. By reading witness statements and circumstantial clues, you must deduce the exact location of every suspect and the victim to crack the case.

## How it Works

`murdoku-solver` translates the board layout, room boundaries, impassable cells, rook distinctness, and natural language clues into first-order logic constraints evaluated by Microsoft's [Z3 SMT solver](https://github.com/Z3Prover/z3). If a unique or valid configuration exists, the solver returns the exact coordinates for every character.

---

## Installation

Ensure you have Python 3.10+ installed. Clone this repository and install it in editable mode:

```bash
# Clone the repository
git clone https://github.com/martineberlein/murdoku-solver.git
cd murdoku-solver

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and package
pip install -e .
```

---

## Quickstart

Run the bundled example script:

```bash
python example.py
```

### Python API Example

```python
from murdoku_solver import (
    AloneWithVictim,
    BoardLayout,
    EastOf,
    InRoom,
    MurdokuEngine,
    OnCategory,
    Person,
)

# 1. Define the board layout (4x4)
layout = BoardLayout(width=4, height=4)
layout.add_room("NorthWing", [(r, c) for r in range(2) for c in range(4)])
layout.add_room("SouthWing", [(r, c) for r in range(2, 4) for c in range(4)])

# 2. Add objects and obstacles
layout.add_object("FloralRug", "rug", [(0, 0), (0, 1)], passable=True)
layout.add_object("Pillar", "rock", [(2, 2)], passable=False)

# 3. Define the characters
people = [
    Person("Victim", is_victim=True),
    Person("Alice"),
    Person("Bob"),
]

# 4. Define the clues
clues = [
    OnCategory("Victim", "rug"),       # Victim must be at (0, 0) or (0, 1)
    InRoom("Alice", "NorthWing"),      # Alice is in the NorthWing
    AloneWithVictim("Victim"),         # Exactly one suspect in the victim's room
    EastOf("Bob", "Alice"),            # Bob's column > Alice's column
]

# 5. Solve
engine = MurdokuEngine(layout, people, clues)
solution = engine.solve()

print("Solution:", solution)
# Output: {'Victim': (0, 1), 'Alice': (1, 0), 'Bob': (2, 3)}
```

- Official Murdoku Game: [murdoku.com/play](https://murdoku.com/play)
- Z3 Theorem Prover: [github.com/Z3Prover/z3](https://github.com/Z3Prover/z3)
