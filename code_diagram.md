# Tic Tac Toe Game - Code Diagram

This UML code diagram is derived from the sequence diagrams, system context diagram, container diagram, and component diagram.

```mermaid
classDiagram
    direction LR

    class GameEngine {
        -GameLoopController gameLoopController
        -GameStateManager gameStateManager
        -PlayerInterface playerInterface
        +startNewGame()
    }

    class GameLoopController {
        -TurnController turnController
        -MoveValidator moveValidator
        -GameStateManager gameStateManager
        -PlayerInterface playerInterface
        +start()
        +runUntilFinished()
        +processMove(Move move)
    }

    class TurnController {
        -PlayerType currentTurn
        +getCurrentTurn() PlayerType
        +switchTurn()
        +isHumanTurn() bool
        +isAITurn() bool
    }

    class MoveValidator {
        +validate(Move move, Board board) ValidationResult
        -isInsideBoard(Position position) bool
        -isPositionAvailable(Position position, Board board) bool
    }

    class OutcomeChecker {
        +checkOutcome(Board board, PlayerType currentPlayer) GameOutcome
        -hasWinningRow(Board board, Mark mark) bool
        -hasWinningColumn(Board board, Mark mark) bool
        -hasWinningDiagonal(Board board, Mark mark) bool
        -isDraw(Board board) bool
    }

    class GameStateManager {
        -Board board
        -GameOutcome outcome
        +initializeBoard()
        +getBoard() Board
        +applyMove(Move move)
        +updateOutcome(GameOutcome outcome)
        +getOutcome() GameOutcome
        +isGameFinished() bool
    }

    class PlayerInterface {
        +promptHumanMove(Board board) Move
        +requestAIMove(Board board) Move
        +showBoard(Board board)
        +showInvalidMoveMessage()
        +showGameState(GameOutcome outcome)
        +showResult(GameOutcome outcome)
    }

    class Board {
        -Cell[3][3] cells
        +initialize()
        +getCell(Position position) Cell
        +placeMark(Position position, Mark mark)
        +isPositionAvailable(Position position) bool
        +isFull() bool
    }

    class Cell {
        -Position position
        -Mark mark
        +isEmpty() bool
        +setMark(Mark mark)
    }

    class Move {
        +Position position
        +Mark mark
        +PlayerType playerType
    }

    class Position {
        +int row
        +int column
    }

    class ValidationResult {
        +bool isValid
        +string message
    }

    class Mark {
        <<enumeration>>
        X
        O
        EMPTY
    }

    class PlayerType {
        <<enumeration>>
        HUMAN
        AI
    }

    class GameOutcome {
        <<enumeration>>
        IN_PROGRESS
        WIN
        LOSE
        DRAW
    }

    GameEngine *-- GameLoopController
    GameEngine *-- GameStateManager
    GameEngine *-- PlayerInterface

    GameLoopController --> TurnController : asks whose turn
    GameLoopController --> PlayerInterface : prompts and displays
    GameLoopController --> MoveValidator : validates moves
    GameLoopController --> GameStateManager : initializes and updates state
    GameLoopController --> OutcomeChecker : checks outcome

    TurnController --> PlayerType
    MoveValidator --> ValidationResult
    MoveValidator ..> Board : reads state
    MoveValidator ..> Move : validates
    OutcomeChecker ..> Board : checks lines
    OutcomeChecker --> GameOutcome
    GameStateManager *-- Board
    GameStateManager --> GameOutcome
    GameStateManager ..> Move : applies
    PlayerInterface ..> Move : creates
    PlayerInterface ..> Board : displays
    Board *-- Cell
    Cell *-- Position
    Cell --> Mark
    Move *-- Position
    Move --> Mark
    Move --> PlayerType
```

## Derivation Notes

- `GameEngine` is the top-level application system from the system context diagram.
- `GameLoopController`, `TurnController`, `MoveValidator`, `OutcomeChecker`, and `GameStateManager` come from the component diagram's `Game Engine Core`.
- `PlayerInterface` comes from the container and component diagrams and handles prompting, AI move requests, board display, invalid move messages, game state, and results.
- `Board`, `Cell`, `Move`, `Position`, `Mark`, `PlayerType`, `ValidationResult`, and `GameOutcome` are code-level domain types inferred from the sequence steps for board initialization, move validation, board updates, and win/lose/draw checks.
- `GameStateManager` owns board mutation because the latest component diagram routes board updates through the state manager and board model.
