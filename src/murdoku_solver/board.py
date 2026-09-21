from collections import defaultdict, deque
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

    @classmethod
    def from_matrix(cls, matrix: list[list[str]]) -> "BoardLayout":
        if not matrix or not matrix[0]:
            return cls(width=0, height=0)

        height = len(matrix)
        width = len(matrix[0])
        layout = cls(width=width, height=height)

        rooms = flood(matrix)
        for key, cells in rooms.items():
            layout.add_room(key, cells)

        return layout


def flood(matrix):
    if not matrix or not matrix[0]:
        return {}

    m, n = len(matrix), len(matrix[0])
    seen = set()
    rooms = defaultdict(list)

    for i in range(m):
        for j in range(n):
            if (i, j) not in seen:
                label = matrix[i][j]
                cells = bfs((i, j), matrix, seen)
                if label is not None and label != "":
                    rooms[label].extend(cells)

    return dict(rooms)


def bfs(start, matrix, seen):
    m, n = len(matrix), len(matrix[0])
    target = matrix[start[0]][start[1]]

    dq = deque([start])
    seen.add(start)
    component = []

    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while dq:
        r, c = dq.popleft()
        component.append((r, c))

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < m
                and 0 <= nc < n
                and (nr, nc) not in seen
                and matrix[nr][nc] == target
            ):
                seen.add((nr, nc))
                dq.append((nr, nc))

    return component
