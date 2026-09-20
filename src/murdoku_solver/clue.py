from abc import ABC, abstractmethod
import z3


from murdoku_solver.context import SolverContext


class Clue(ABC):
    @abstractmethod
    def apply(self, ctx: SolverContext):
        """Translate clue into Z3 constraints."""


class EastOf(Clue):
    def __init__(self, person_a: str, person_b: str):
        self.a, self.b = person_a, person_b

    def apply(self, ctx: SolverContext):
        ctx.solver.add(ctx.c[self.a] > ctx.c[self.b])


class InSameRoom(Clue):
    def __init__(self, person_a: str, person_b: str):
        self.a, self.b = person_a, person_b

    def apply(self, ctx: SolverContext):
        ctx.solver.add(
            ctx.room_fn(ctx.r[self.a], ctx.c[self.a])
            == ctx.room_fn(ctx.r[self.b], ctx.c[self.b])
        )


class OnCategory(Clue):
    def __init__(self, person: str, category: str):
        self.person, self.category = person, category

    def apply(self, ctx: SolverContext):
        cells = [
            (r, c)
            for obj in ctx.layout.objects.values()
            if obj.category == self.category
            for r, c in obj.cells
        ]
        pr, pc = ctx.r[self.person], ctx.c[self.person]
        ctx.solver.add(z3.Or([z3.And(pr == r, pc == c) for r, c in cells]))


class InRoom(Clue):
    def __init__(self, person: str, room: str):
        self.person = person
        self.room = room

    def apply(self, ctx: SolverContext):
        rid = ctx.room_ids[self.room]
        ctx.solver.add(ctx.room_fn(ctx.r[self.person], ctx.c[self.person]) == rid)


class AloneWithVictim(Clue):
    def __init__(self, victim: str, suspect: str | None = None):
        self.victim = victim
        self.suspect = suspect

    def apply(self, ctx: SolverContext):
        v_room = ctx.room_fn(ctx.r[self.victim], ctx.c[self.victim])
        suspects = [
            name
            for name, p in ctx.people.items()
            if name != self.victim and not p.is_victim
        ]
        if not suspects:
            suspects = [name for name in ctx.people if name != self.victim]

        if self.suspect:
            ctx.solver.add(
                ctx.room_fn(ctx.r[self.suspect], ctx.c[self.suspect]) == v_room
            )

        ctx.solver.add(
            z3.Sum(
                [
                    z3.If(ctx.room_fn(ctx.r[s], ctx.c[s]) == v_room, 1, 0)
                    for s in suspects
                ]
            )
            == 1
        )

