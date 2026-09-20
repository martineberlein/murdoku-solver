from murdoku_solver import (
    AloneWithVictim,
    BoardLayout,
    EastOf,
    InRoom,
    MurdokuEngine,
    OnCategory,
    Person,
)

if __name__ == "__main__":
    # 4x4 layout: North (rows 0-1) vs South (rows 2-3)
    layout = BoardLayout(width=4, height=4)
    layout.add_room("NorthWing", [(r, c) for r in range(2) for c in range(4)])
    layout.add_room("SouthWing", [(r, c) for r in range(2, 4) for c in range(4)])
    layout.add_object("FloralRug", "rug", [(0, 0), (0, 1)], passable=True)
    layout.add_object("Pillar", "rock", [(2, 2)], passable=False)

    people = [
        Person("Victim", is_victim=True),
        Person("Alice"),
        Person("Bob"),
    ]

    clues = [
        OnCategory("Victim", "rug"),       # Victim must be at (0, 0) or (0, 1)
        InRoom("Alice", "NorthWing"),      # Alice is in the NorthWing
        AloneWithVictim("Victim"),         # Only one suspect in NorthWing -> Bob forced to SouthWing
        EastOf("Bob", "Alice"),            # Bob's column > Alice's column
    ]

    engine = MurdokuEngine(layout, people, clues)
    solution = engine.solve()
    print("Solution:", solution)
