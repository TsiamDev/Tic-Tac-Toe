# Tic Tac Toe Game - Container Diagram

This container diagram is derived from the sequence diagrams and system context diagram.

```mermaid
C4Container
    title Container Diagram - Tic Tac Toe Game

    Person(player, "Player", "A person who plays Tic Tac Toe")
    Person(ai, "AI Player", "A computer-controlled player that makes automated moves")

    System_Boundary(engine, "GameEngine") {
        Container(gameEngine, "Game Engine Core", "Application Component", "Validates moves, updates board state, checks win/lose/draw conditions, and manages game state")
        Container(boardModel, "Board Model", "In-Memory Domain Model", "Stores the 3x3 board, occupied positions, marks, and available moves")
        Container(playerInterface, "Player Interface", "Application Component", "Prompts for player moves and displays the board, invalid move messages, game state, and game outcomes")
    }

    Rel(player, playerInterface, "Sends input")
    Rel(playerInterface, player, "Displays board, game state, invalid move messages, and win/lose/draw result")

    Rel(gameEngine, boardModel, "Reads and updates board state")
    Rel(gameEngine, playerInterface, "Requests input and display output")

    Rel(ai, playerInterface, "Makes automated moves")
    Rel(playerInterface, ai, "Requests AI move selection")
```

## Derivation Notes

- `GameEngine` is the system boundary from the updated system context diagram.
- `Game Engine Core` comes from the central sequence participant responsible for starting games, turn flow, move validation, board updates, and result checks.
- `Board Model` is derived from the repeated board initialization, move validation, state updates, and row/column/diagonal checks.
- `Player Interface` represents the prompts, board display, invalid move message, and result display shown in the sequence diagrams.
