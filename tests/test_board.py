import unittest

from murdoku_solver.board import BoardLayout


class TestBoard(unittest.TestCase):
    def test_board_from_matrix(self):
        board_plan = [
            [
                "Garden",
                "Garden",
                "Garden",
            ],
            ["House", "House", "House"],
        ]

        layout = BoardLayout.from_matrix(board_plan)
        self.assertEqual(layout.width, 3)
        self.assertEqual(layout.height, 2)
        self.assertIn("Garden", layout.rooms)
        self.assertIn("House", layout.rooms)
        self.assertEqual(layout.rooms["Garden"].cells, [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(layout.rooms["House"].cells, [(1, 0), (1, 1), (1, 2)])


if __name__ == "__main__":
    unittest.main()
