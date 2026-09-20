from __future__ import annotations

from typing import TYPE_CHECKING
from murdoku_solver.board import BoardLayout
from murdoku_solver.person import Person

if TYPE_CHECKING:
    from murdoku_solver.engine import MurdokuEngine


class SolutionPrinter:
    """Formats and prints solutions for Murdoku puzzle cases."""

    def __init__(
        self,
        layout: BoardLayout,
        people: list[Person] | dict[str, Person],
    ):
        self.layout = layout
        if isinstance(people, list):
            self.people = {p.name: p for p in people}
        else:
            self.people = people

    @classmethod
    def from_engine(cls, engine: MurdokuEngine) -> SolutionPrinter:
        """Constructs a printer directly from a MurdokuEngine instance."""
        return cls(engine.ctx.layout, engine.ctx.people)

    def find_victim_and_murderer(
        self, solution: dict[str, tuple[int, int]]
    ) -> tuple[str | None, str | None, str | None]:
        """Finds (victim_name, victim_room_name, murderer_name) from solution."""
        victim_name = next(
            (name for name, p in self.people.items() if p.is_victim), None
        )
        if not victim_name:
            return None, None, None

        victim_coords = solution.get(victim_name)
        if not victim_coords:
            return victim_name, None, None

        victim_room = None
        for rname, room in self.layout.rooms.items():
            if victim_coords in room.cells:
                victim_room = rname
                break

        murderer_name = None
        if victim_room:
            room = self.layout.rooms.get(victim_room)
            for name, coords in solution.items():
                if name != victim_name and room and coords in room.cells:
                    murderer_name = name
                    break

        return victim_name, victim_room, murderer_name

    def format_grid(self, solution: dict[str, tuple[int, int]]) -> str:
        """Formats the ASCII board grid with character initials."""
        grid = [
            [" . " for _ in range(self.layout.width)]
            for _ in range(self.layout.height)
        ]
        for name, (r, c) in solution.items():
            if 0 <= r < self.layout.height and 0 <= c < self.layout.width:
                grid[r][c] = f" {name[0]} "

        lines = []
        header = "   " + " ".join(f"C{c}" for c in range(self.layout.width))
        lines.append(header)
        for r in range(self.layout.height):
            lines.append(f"R{r} " + "".join(grid[r]))
        return "\n".join(lines)

    def format_solution(
        self,
        solution: dict[str, tuple[int, int]] | None,
        title: str | None = None,
    ) -> str:
        """Formats full solution output including coordinates, grid, and case deduction."""
        lines: list[str] = []
        if title:
            lines.append(f"=== {title} ===")

        if solution is None:
            lines.append("No solution found.")
            return "\n".join(lines)

        lines.append("Solution found:")
        max_name_len = max(len(name) for name in solution) if solution else 0
        for name, coords in sorted(solution.items()):
            p = self.people.get(name)
            role = "Victim" if (p and p.is_victim) else "Suspect"
            lines.append(
                f"  {name:{max_name_len}s} ({role:7s}): Row {coords[0]}, Col {coords[1]}"
            )

        lines.append("")
        lines.append(
            f"Grid (R0-R{self.layout.height-1} top to bottom, C0-C{self.layout.width-1} left to right):"
        )
        lines.append(self.format_grid(solution))

        victim, room, murderer = self.find_victim_and_murderer(solution)
        if victim and room:
            lines.append("")
            lines.append(f"Victim {victim} was in the {room}.")
            if murderer:
                lines.append(f"The murderer alone with {victim} was: {murderer}!")

        return "\n".join(lines)

    def print_solution(
        self,
        solution: dict[str, tuple[int, int]] | None,
        title: str | None = None,
    ) -> None:
        """Prints formatted solution to stdout."""
        print(self.format_solution(solution, title=title))
