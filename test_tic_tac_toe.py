import unittest

from tic_tac_toe import (
    Board,
    GameOutcome,
    GameStateManager,
    Mark,
    Move,
    MoveValidator,
    OutcomeChecker,
    PlayerType,
    Position,
    TurnController,
)


class MoveValidatorTests(unittest.TestCase):
    def test_valid_move_on_empty_board(self) -> None:
        board = Board()
        move = Move(Position(0, 0), Mark.X, PlayerType.HUMAN)

        result = MoveValidator().validate(move, board)

        self.assertTrue(result.is_valid)

    def test_rejects_occupied_position(self) -> None:
        board = Board()
        board.place_mark(Position(0, 0), Mark.X)
        move = Move(Position(0, 0), Mark.O, PlayerType.AI)

        result = MoveValidator().validate(move, board)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.message, "Position is already occupied.")

    def test_rejects_out_of_bounds_position(self) -> None:
        board = Board()
        move = Move(Position(3, 0), Mark.X, PlayerType.HUMAN)

        result = MoveValidator().validate(move, board)

        self.assertFalse(result.is_valid)
        self.assertEqual(result.message, "Position must be between 1 and 3.")


class OutcomeCheckerTests(unittest.TestCase):
    def test_detects_human_win(self) -> None:
        board = Board()
        board.place_mark(Position(0, 0), Mark.X)
        board.place_mark(Position(0, 1), Mark.X)
        board.place_mark(Position(0, 2), Mark.X)

        outcome = OutcomeChecker().check_outcome(board, PlayerType.HUMAN)

        self.assertEqual(outcome, GameOutcome.WIN)

    def test_detects_ai_win_as_loss(self) -> None:
        board = Board()
        board.place_mark(Position(0, 0), Mark.O)
        board.place_mark(Position(1, 1), Mark.O)
        board.place_mark(Position(2, 2), Mark.O)

        outcome = OutcomeChecker().check_outcome(board, PlayerType.AI)

        self.assertEqual(outcome, GameOutcome.LOSE)

    def test_detects_draw(self) -> None:
        board = Board()
        marks = [
            [Mark.X, Mark.O, Mark.X],
            [Mark.X, Mark.O, Mark.O],
            [Mark.O, Mark.X, Mark.X],
        ]
        for row_index, row in enumerate(marks):
            for column_index, mark in enumerate(row):
                board.place_mark(Position(row_index, column_index), mark)

        outcome = OutcomeChecker().check_outcome(board, PlayerType.HUMAN)

        self.assertEqual(outcome, GameOutcome.DRAW)


class GameStateManagerTests(unittest.TestCase):
    def test_apply_move_updates_board(self) -> None:
        state = GameStateManager()
        move = Move(Position(1, 1), Mark.X, PlayerType.HUMAN)

        state.apply_move(move)

        self.assertEqual(state.get_board().get_cell(Position(1, 1)).mark, Mark.X)


class TurnControllerTests(unittest.TestCase):
    def test_switch_turn_alternates_players(self) -> None:
        turn_controller = TurnController()

        self.assertTrue(turn_controller.is_human_turn())
        turn_controller.switch_turn()
        self.assertTrue(turn_controller.is_ai_turn())
        turn_controller.switch_turn()
        self.assertTrue(turn_controller.is_human_turn())


if __name__ == "__main__":
    unittest.main()
