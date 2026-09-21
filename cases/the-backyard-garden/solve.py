"""Solver for Murdoku Case: The Backyard Garden (9x9).

Screenshot: cases/the-backyard-garden/the-backyard-garden.png
"""

from murdoku_solver import (
    Alone,
    AloneWithVictim,
    BesideCategory,
    BoardLayout,
    InRoom,
    InSameRoom,
    MurdokuEngine,
    OnCategory,
    Person,
    SolutionPrinter,
)


def solve_backyard_garden():
    labels = {
        1: "Backyard",
        2: "Pond",
        3: "Garden",
        4: "Shed",
        5: "Sunroom",
        6: "Bedroom",
        7: "LivingRoom",
        8: "Kitchen",
    }

    matrix = [
        [1, 1, 1, 2, 2, 2, 1, 3, 3],
        [1, 1, 2, 2, 2, 2, 1, 3, 3],
        [1, 1, 2, 1, 1, 1, 1, 3, 3],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [4, 4, 4, 1, 5, 5, 5, 5, 5],
        [4, 1, 1, 1, 5, 5, 5, 5, 5],
        [1, 1, 6, 7, 7, 7, 8, 8, 8],
        [6, 6, 6, 7, 7, 7, 8, 8, 8],
        [6, 6, 6, 7, 7, 7, 8, 8, 8],
    ]

    string_matrix = [[labels[val] for val in row] for row in matrix]
    layout = BoardLayout.from_matrix(string_matrix)

    # Chairs (passable)
    layout.add_object("SunroomChair1", "chair", [(4, 5)], passable=True)
    layout.add_object("SunroomChair2", "chair", [(4, 7)], passable=True)
    layout.add_object("SunroomChair3", "chair", [(5, 4)], passable=True)
    layout.add_object("LivingRoomChair", "chair", [(8, 4)], passable=True)

    # Trees (impassable)
    layout.add_object("BackyardTree1", "tree", [(0, 1)], passable=False)
    layout.add_object("BackyardTree2", "tree", [(2, 5)], passable=False)

    # Carpets (passable)
    layout.add_object("SunroomCarpet", "carpet", [(5, 5), (5, 6)], passable=True)
    layout.add_object("BedroomCarpet", "carpet", [(7, 2), (8, 2)], passable=True)
    layout.add_object(
        "KitchenCarpet", "carpet", [(7, 6), (7, 7), (8, 6)], passable=True
    )

    # Tables (impassable)
    layout.add_object("GardenTable", "table", [(3, 8)], passable=False)
    layout.add_object("SunroomTable", "table", [(4, 6)], passable=False)
    layout.add_object("BedroomTable", "table", [(7, 1)], passable=False)
    layout.add_object("LivingRoomTable", "table", [(7, 3)], passable=False)

    # Flowers / Bushes (impassable)
    layout.add_object("GardenFlowers1", "flowers", [(0, 7)], passable=False)
    layout.add_object("GardenFlowers2", "flowers", [(2, 7)], passable=False)
    layout.add_object("BackyardFlowers1", "flowers", [(3, 0)], passable=False)
    layout.add_object("BackyardFlowers2", "flowers", [(3, 6)], passable=False)
    layout.add_object("BackyardFlowers3", "flowers", [(6, 1)], passable=False)

    # Shelves / Bookcases / Cabinets (impassable)
    layout.add_object("ShedShelf", "shelf", [(4, 0)], passable=False)
    layout.add_object("LivingRoomShelf1", "shelf", [(6, 3)], passable=False)
    layout.add_object("LivingRoomShelf2", "shelf", [(6, 5)], passable=False)
    layout.add_object("KitchenShelf", "shelf", [(8, 7)], passable=False)
    layout.add_object("KitchenCabinet", "shelf", [(7, 8), (8, 8)], passable=False)

    # Bed (impassable)
    layout.add_object("Bed", "bed", [(8, 0), (8, 1)], passable=False)

    # Stereo / Music Player (impassable)
    layout.add_object("Stereo", "stereo", [(6, 4)], passable=False)

    people = [
        Person("Aaron"),
        Person("Bruce"),
        Person("Carissa"),
        Person("Denise"),
        Person("Elyse"),
        Person("Franklin"),
        Person("Gilbert"),
        Person("Holden"),
        Person("Violet", is_victim=True),
    ]

    clues = [
        InRoom("Aaron", "LivingRoom"),  # "He was with Elyse in the Living Room."
        InSameRoom("Aaron", "Elyse"),
        InRoom("Bruce", "Shed"),  # "He was in the Shed."
        BesideCategory("Carissa", "tree"),  # "She was beside a tree."
        InRoom(
            "Denise", ["Bedroom", "Sunroom"]
        ),  # "She was in the Bedroom or in the Sunroom."
        OnCategory("Elyse", "chair"),  # "She was sitting on a chair."
        OnCategory("Franklin", "carpet"),  # "He was on a carpet."
        InRoom("Gilbert", "Garden"),  # "He was in the Garden."
        Alone("Holden"),  # "He was alone."
        AloneWithVictim("Violet"),  # "The Victim. She was alone with the murderer."
    ]

    # --- Solve ---
    engine = MurdokuEngine(layout, people, clues)
    solution = engine.solve()

    printer = SolutionPrinter(layout, people)
    printer.print_solution(solution, title="Case: The Backyard Garden (9x9)")

    return solution


if __name__ == "__main__":
    solve_backyard_garden()
