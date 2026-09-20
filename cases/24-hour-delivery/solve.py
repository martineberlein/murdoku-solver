"""Solver for Murdoku Case: 24-Hour Delivery (6x6).

Screenshot: cases/24-hour-delivery/screenshot.png
"""

from murdoku_solver import (
    AloneWithVictim,
    BesideCategory,
    BoardLayout,
    InRoom,
    MurdokuEngine,
    OnCategory,
    OnlyPersonOnCategory,
    Person,
    SolutionPrinter,
)


def solve_24_hour_delivery():
    # 6x6 Board Layout
    layout = BoardLayout(width=6, height=6)

    # 1. Rooms
    layout.add_room("DiningRoom", [(r, c) for r in range(4) for c in range(3)])
    layout.add_room("Bedroom", [(r, c) for r in range(2) for c in range(3, 6)])
    layout.add_room("Kitchen", [(r, c) for r in range(2, 4) for c in range(3, 6)])
    layout.add_room("Porch", [(r, c) for r in range(4, 6) for c in range(2)])
    layout.add_room("FrontYard", [(r, c) for r in range(4, 6) for c in range(2, 6)])

    # 2. Objects & Furniture
    # Chairs (passable)
    layout.add_object("DiningChairHead", "chair", [(0, 1)], passable=True)
    layout.add_object("DiningChairLeft1", "chair", [(1, 0)], passable=True)
    layout.add_object("DiningChairLeft2", "chair", [(2, 0)], passable=True)
    layout.add_object("PorchChair", "chair", [(5, 1)], passable=True)

    # Impassable furniture / obstacles
    layout.add_object("DiningTable", "table", [(1, 1), (2, 1)], passable=False)
    layout.add_object("Bed", "bed", [(0, 3), (0, 4)], passable=False)
    layout.add_object("KitchenCounter", "table", [(3, 3), (3, 4)], passable=False)

    # Plants & Shrubs (impassable)
    layout.add_object("DiningPlant", "plant", [(3, 0)], passable=False)
    layout.add_object("BedroomPlant", "plant", [(1, 4)], passable=False)
    layout.add_object("YardShrub1", "shrub", [(4, 3)], passable=False)
    layout.add_object("YardShrub2", "shrub", [(5, 4)], passable=False)

    # Delivery Box (on the Porch)
    layout.add_object("DeliveryBox", "box", [(4, 0)], passable=False)

    # Carpets (passable)
    layout.add_object("BedroomCarpet", "carpet", [(0, 5), (1, 5)], passable=True)
    layout.add_object("KitchenCarpet", "carpet", [(2, 3), (2, 4)], passable=True)
    layout.add_object("PorchCarpet", "carpet", [(4, 1)], passable=True)

    # 3. People (Suspects + Victim)
    people = [
        Person("Alexander"),
        Person("Bella"),
        Person("Carol"),
        Person("Dalia"),
        Person("Evangeline"),
        Person("Viraj", is_victim=True),
    ]

    # 4. Clues from the case
    clues = [
        BesideCategory("Alexander", "box"),  # "He was beside the box."
        OnCategory("Bella", "chair"),  # "She was sitting in a chair."
        OnlyPersonOnCategory(
            "Carol", "carpet"
        ),  # "She was the only person on a carpet."
        InRoom("Dalia", "Bedroom"),  # "She was in the Bedroom."
        BesideCategory(
            "Evangeline", ["shrub", "plant"]
        ),  # "She was either beside a shrub or a plant."
        AloneWithVictim(
            "Viraj"
        ),  # "The Victim. He was alone with the murderer."
    ]

    # 5. Solve
    engine = MurdokuEngine(layout, people, clues)
    solution = engine.solve()

    printer = SolutionPrinter(layout, people)
    printer.print_solution(solution, title="Case: 24-Hour Delivery (6x6)")

    return solution


if __name__ == "__main__":
    solve_24_hour_delivery()
