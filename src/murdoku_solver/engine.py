from z3 import sat
from murdoku_solver.board import BoardLayout
from murdoku_solver.person import Person
from murdoku_solver.clue import Clue
from murdoku_solver.context import SolverContext


class MurdokuEngine:
    def __init__(self, layout: BoardLayout, people: list[Person], clues: list[Clue]):
        self.ctx = SolverContext(layout, people)
        self.clues = clues

    def solve(self) -> dict[str, tuple[int, int]] | None:
        self.ctx.compile_base_physics()
        for clue in self.clues:
            clue.apply(self.ctx)

        if self.ctx.solver.check() == sat:
            m = self.ctx.solver.model()
            return {
                name: (m[self.ctx.r[name]].as_long(), m[self.ctx.c[name]].as_long())
                for name in self.ctx.people
            }
        return None
