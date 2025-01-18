# Gomoku-HDC

## Gomoku Game

**Gomoku** is a classic **Five in a Row** game traditionally played with **Go** pieces (black and white stones) on a **15x15 Go board**. The objective of the game is to be the first to form an unbroken row of five stones horizontally, vertically, or diagonally.

Players take turns to place their stones on the empty intersections of the board, aiming to create a line of five stones of the same color while preventing their opponent from doing the same.


## Hyperdimentional Computing (HDC)
### Encoding the Gomoku Board HDC

In this project, the **Gomoku** game board is represented using a high-dimensional encoding approach. The state of the board is encoded as a superposition of high-dimensional vectors that capture both the positions of the pieces on the board and the corresponding turns of the players.

The encoding is defined as:

$$
|Board\rangle = \bigoplus_{k=0}^{n} \left( |(x_i, y_j)\rangle \otimes |t_{k \mod 2}\rangle \right)
$$

Where:
- n is the number of turns played so far in the game.
- $(x_i, y_j)$ represents the coordinates on the Gomoku board where a piece has been placed.
- $t_k$ is the symbol representing the player's move at turn k, with $t_k$ in black, and white.
- $\bigoplus$ denotes the **hyperdimensional addition** (or binding) operation, which is used to combine the individual components into a high-dimensional vector.
- $\otimes$ denotes the **tensor product**, used to combine the positional vector $|(x_i, y_j)\rangle$ with the player's turn vector $|t_{k \mod 2}\rangle$.
