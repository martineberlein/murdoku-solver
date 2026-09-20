from dataclasses import dataclass, field


@dataclass
class BoardObject:
    name: str
    category: str
    cells: list[tuple[int, int]]
    passable: bool = True


@dataclass
class Room:
    name: str
    cells: list[tuple[int, int]]


@dataclass
class BoardLayout:
    width: int
    height: int
    rooms: dict[str, Room] = field(default_factory=dict)
    objects: dict[str, BoardObject] = field(default_factory=dict)

    def add_room(self, name: str, cells: list[tuple[int, int]]):
        self.rooms[name] = Room(name, cells)

    def add_object(
        self,
        name: str,
        category: str,
        cells: list[tuple[int, int]],
        passable: bool = True,
    ):
        self.objects[name] = BoardObject(name, category, cells, passable)
