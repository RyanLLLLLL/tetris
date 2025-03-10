# tetris-module
## This module handles the game logic for a tetris game on a classic 10 x 20 grid.

- To start, import with "from tetris import tetrisGame".

- To setup a game, assign "tetrisGame()" as a variable to access later.
	- example: game = tetrisGame()

- Call "game.update()" 60 times per second
- At any time, call:
	- "game.left()" to move piece left
	- "game.right()" to move piece right
	- "game.down()" to move piece down once
	- "game.up()" to move piece down to bottom
	- "game.rotate()" to rotate piece right
	
- The use these variables to get info about the game:
	- "game.grid[x][y]['color']" to get the color of a piece at (x, y) in a (r, g, b) format
	- "game.score" to get a int of the current score
	- "game.lines" to get a int of the number of lines cleared
	- "game.level" to get a int of the current level
	- "game.game_over" to get a bool of if the game is over
	- "game.bag" is a list of at least the next 10 pieces in the same format found in data.py
