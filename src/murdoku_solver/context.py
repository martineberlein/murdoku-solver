import z3
from murdoku_solver.person import Person
from murdoku_solver.board import BoardLayout


class SolverContext:
    def __init__(self, layout: BoardLayout, people: list[Person]):
        self.layout = layout
        self.people = {p.name: p for p in people}
        self.solver = z3.Solver()

        # Z3 coordinate variables
        self.r = {p.name: z3.Int(f"{p.name}_r") for p in people}
        self.c = {p.name: z3.Int(f"{p.name}_c") for p in people}

        # Room mapping lookup
        self.room_fn = z3.Function("room_of", z3.IntSort(), z3.IntSort(), z3.IntSort())
        self.room_ids = {name: i for i, name in enumerate(layout.rooms)}
        for name, room in layout.rooms.items():
            rid = self.room_ids[name]
            for r, c in room.cells:
                self.solver.add(self.room_fn(r, c) == rid)

    def compile_base_physics(self):
        """Enforces boundaries, rook distinctness, and impassable cells."""
        plist = list(self.people.values())
        for p in plist:
            self.solver.add(self.r[p.name] >= 0, self.r[p.name] < self.layout.height)
            self.solver.add(self.c[p.name] >= 0, self.c[p.name] < self.layout.width)

        self.solver.add(z3.Distinct(list(self.r.values())))
        self.solver.add(z3.Distinct(list(self.c.values())))

        for obj in self.layout.objects.values():
            if not obj.passable:
                for p in plist:
                    for r, c in obj.cells:
                        self.solver.add(
                            z3.Not(z3.And(self.r[p.name] == r, self.c[p.name] == c))
                        )
