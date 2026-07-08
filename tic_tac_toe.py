from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class Mark(Enum):
    X = "X"
    O = "O"
    EMPTY = " "


class PlayerType(Enum):
    HUMAN = "human"
    AI = "ai"


class GameOutcome(Enum):
    IN_PROGRESS = "in_progress"
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


@dataclass(frozen=True)
class Position:
    row: int
    column: int


@dataclass(frozen=True)
class Move:
    position: Position
    mark: Mark
    player_type: PlayerType


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    message: str = ""


@dataclass
class Cell:
    position: Position
    mark: Mark = Mark.EMPTY

    def is_empty(self) -> bool:
        return self.mark is Mark.EMPTY

    def set_mark(self, mark: Mark) -> None:
        if not self.is_empty():
            raise ValueError("Cell is already marked.")
        self.mark = mark


class Board:
    size = 3

    def __init__(self) -> None:
        self.cells: list[list[Cell]] = []
        self.initialize()

    def initialize(self) -> None:
        self.cells = [
            [Cell(Position(row, column)) for column in range(self.size)]
            for row in range(self.size)
        ]

    def get_cell(self, position: Position) -> Cell:
        return self.cells[position.row][position.column]

    def place_mark(self, position: Position, mark: Mark) -> None:
        self.get_cell(position).set_mark(mark)

    def is_position_available(self, position: Position) -> bool:
        return self.get_cell(position).is_empty()

    def is_full(self) -> bool:
        return all(not cell.is_empty() for row in self.cells for cell in row)

    def available_positions(self) -> list[Position]:
        return [
            cell.position
            for row in self.cells
            for cell in row
            if cell.is_empty()
        ]

    def render(self) -> str:
        rows = []
        for row in self.cells:
            rows.append(" | ".join(cell.mark.value for cell in row))
        return "\n---------\n".join(rows)


class TurnController:
    def __init__(self) -> None:
        self.current_turn = PlayerType.HUMAN

    def get_current_turn(self) -> PlayerType:
        return self.current_turn

    def switch_turn(self) -> None:
        if self.current_turn is PlayerType.HUMAN:
            self.current_turn = PlayerType.AI
        else:
            self.current_turn = PlayerType.HUMAN

    def is_human_turn(self) -> bool:
        return self.current_turn is PlayerType.HUMAN

    def is_ai_turn(self) -> bool:
        return self.current_turn is PlayerType.AI


class MoveValidator:
    def validate(self, move: Move, board: Board) -> ValidationResult:
        if not self._is_inside_board(move.position):
            return ValidationResult(False, "Position must be between 1 and 3.")
        if not self._is_position_available(move.position, board):
            return ValidationResult(False, "Position is already occupied.")
        return ValidationResult(True)

    def _is_inside_board(self, position: Position) -> bool:
        return 0 <= position.row < Board.size and 0 <= position.column < Board.size

    def _is_position_available(self, position: Position, board: Board) -> bool:
        return board.is_position_available(position)


class OutcomeChecker:
    def check_outcome(self, board: Board, current_player: PlayerType) -> GameOutcome:
        mark = Mark.X if current_player is PlayerType.HUMAN else Mark.O
        if (
            self._has_winning_row(board, mark)
            or self._has_winning_column(board, mark)
            or self._has_winning_diagonal(board, mark)
        ):
            return GameOutcome.WIN if current_player is PlayerType.HUMAN else GameOutcome.LOSE
        if self._is_draw(board):
            return GameOutcome.DRAW
        return GameOutcome.IN_PROGRESS

    def _has_winning_row(self, board: Board, mark: Mark) -> bool:
        return any(all(cell.mark is mark for cell in row) for row in board.cells)

    def _has_winning_column(self, board: Board, mark: Mark) -> bool:
        return any(
            all(board.cells[row][column].mark is mark for row in range(Board.size))
            for column in range(Board.size)
        )

    def _has_winning_diagonal(self, board: Board, mark: Mark) -> bool:
        left_to_right = all(board.cells[index][index].mark is mark for index in range(Board.size))
        right_to_left = all(
            board.cells[index][Board.size - 1 - index].mark is mark
            for index in range(Board.size)
        )
        return left_to_right or right_to_left

    def _is_draw(self, board: Board) -> bool:
        return board.is_full()


class GameStateManager:
    def __init__(self) -> None:
        self.board = Board()
        self.outcome = GameOutcome.IN_PROGRESS

    def initialize_board(self) -> None:
        self.board.initialize()
        self.outcome = GameOutcome.IN_PROGRESS

    def get_board(self) -> Board:
        return self.board

    def apply_move(self, move: Move) -> None:
        self.board.place_mark(move.position, move.mark)

    def update_outcome(self, outcome: GameOutcome) -> None:
        self.outcome = outcome

    def get_outcome(self) -> GameOutcome:
        return self.outcome

    def is_game_finished(self) -> bool:
        return self.outcome is not GameOutcome.IN_PROGRESS


class PlayerInterface:
    def prompt_human_move(self, board: Board) -> Move:
        while True:
            raw_value = input("Choose a board position as row,column (1-3): ").strip()
            try:
                row_text, column_text = raw_value.split(",", maxsplit=1)
                position = Position(int(row_text) - 1, int(column_text) - 1)
                return Move(position, Mark.X, PlayerType.HUMAN)
            except ValueError:
                print("Use the format row,column. Example: 2,3")

    def request_ai_move(self, board: Board) -> Move:
        position = random.choice(board.available_positions())
        return Move(position, Mark.O, PlayerType.AI)

    def show_board(self, board: Board) -> None:
        print()
        print(board.render())
        print()

    def show_invalid_move_message(self, message: str = "Invalid move.") -> None:
        print(message)

    def show_game_state(self, outcome: GameOutcome) -> None:
        print(f"Game state: {outcome.value}")

    def show_result(self, outcome: GameOutcome) -> None:
        if outcome is GameOutcome.WIN:
            print("You win!")
        elif outcome is GameOutcome.LOSE:
            print("You lose.")
        elif outcome is GameOutcome.DRAW:
            print("Draw.")


class GameLoopController:
    def __init__(
        self,
        turn_controller: TurnController,
        move_validator: MoveValidator,
        outcome_checker: OutcomeChecker,
        game_state_manager: GameStateManager,
        player_interface: PlayerInterface,
    ) -> None:
        self.turn_controller = turn_controller
        self.move_validator = move_validator
        self.outcome_checker = outcome_checker
        self.game_state_manager = game_state_manager
        self.player_interface = player_interface

    def start(self) -> None:
        self.game_state_manager.initialize_board()
        self.player_interface.show_board(self.game_state_manager.get_board())
        self.run_until_finished()

    def run_until_finished(self) -> None:
        while not self.game_state_manager.is_game_finished():
            board = self.game_state_manager.get_board()
            if self.turn_controller.is_human_turn():
                move = self.player_interface.prompt_human_move(board)
            else:
                move = self.player_interface.request_ai_move(board)
            self.process_move(move)
        self.player_interface.show_result(self.game_state_manager.get_outcome())

    def process_move(self, move: Move) -> ValidationResult:
        board = self.game_state_manager.get_board()
        validation = self.move_validator.validate(move, board)
        if not validation.is_valid:
            self.player_interface.show_invalid_move_message(validation.message)
            return validation

        self.game_state_manager.apply_move(move)
        outcome = self.outcome_checker.check_outcome(board, move.player_type)
        self.game_state_manager.update_outcome(outcome)
        self.player_interface.show_board(board)
        self.player_interface.show_game_state(outcome)

        if outcome is GameOutcome.IN_PROGRESS:
            self.turn_controller.switch_turn()
        return validation


class GameEngine:
    def __init__(self, player_interface: PlayerInterface | None = None) -> None:
        self.game_state_manager = GameStateManager()
        self.player_interface = player_interface or PlayerInterface()
        self.game_loop_controller = GameLoopController(
            TurnController(),
            MoveValidator(),
            OutcomeChecker(),
            self.game_state_manager,
            self.player_interface,
        )

    def start_new_game(self) -> None:
        self.game_loop_controller.start()


def main() -> None:
    GameEngine().start_new_game()


if __name__ == "__main__":
    main()
