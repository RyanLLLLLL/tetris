from .data import pieces, speeds
import random

class tetrisGame:
	def __init__(self):
		self.grid = []
		for x in range(10):
			column = []
			for y in range(20):
				column.append({
					'empty': True,
					'color': (0.2, 0.2, 0.2),
					'pos': (x, y)
				})
			self.grid.append(column)
		self.score = 0
		self.level = 0
		self.lines = 0
		
		self.game_over = False
		self.tick_speed = 0
		self.tick_cooldown = 0
		self.set_speed()
		
		self.piece = {
			'cells': [],
			'pos': (0, 0),
			'color': (0.0, 0.0, 0.0),
			'rotation': 0,
			'piece_array': None
		}
		
		self.bag = []
		while len(self.bag) < 10:
			self.refill_bag()
		self.spawn_piece()
		
	def refill_bag(self):
		next_pieces = [item for item in pieces]
		random.shuffle(next_pieces)
		self.bag += next_pieces
		
	def set_speed(self):
		for speed_data in speeds:
			speed_data = speed_data.split('=')
			speed = int(speed_data[1])
			speed_data = speed_data[0].split('-')
			if speed_data[1] == 'inf':
				if self.level >= int(speed_data[0]):
					self.tick_speed = speed
					break
			else:
				if self.level >= int(speed_data[0]) and self.level <= int(speed_data[1]):
					self.tick_speed = speed
					break
		
	def spawn_piece(self):
		piece = pieces[self.bag.pop(0)]
		if len(self.bag) < 10:
			self.refill_bag()
		
		self.piece['piece_array'] = piece['piece_array']
		self.piece['cells'] = []
		self.piece['rotation'] = 0
		self.piece['pos'] = [max(4 - ((len(self.piece['piece_array'][0][0])-1) // 2), 0), 20]
		self.piece['color'] = piece['color']
		size = len(self.piece['piece_array'][0][0])
		min_y = 100
		for y in range(size):
			for x in range(size):
				if self.piece['piece_array'][self.piece['rotation']][size-y-1][x] != '.':
					self.piece['cells'].append((x, y))
					min_y = min(min_y, y)
		self.move_piece(0, -min_y)
					
	def move_piece(self, i, j):
		can_move = True
		for pos in self.piece['cells']:
			x, y = self.piece['pos'][0]+pos[0]+i, self.piece['pos'][1]+pos[1]+j
			if y >= 0 and x >= 0 and x < 10:
				if y < 20:
					if not self.grid[x][y]['empty']:
						can_move = False
						break
			else:
				can_move = False
				break
		if can_move:
			for pos in self.piece['cells']:
				x, y = self.piece['pos'][0]+pos[0], self.piece['pos'][1]+pos[1]
				if y < 20:
					cell = self.grid[x][y]
					cell['color'] = (0.2, 0.2, 0.2)
			self.piece['pos'][0] += i
			self.piece['pos'][1] += j
			for pos in self.piece['cells']:
				x, y = self.piece['pos'][0]+pos[0], self.piece['pos'][1]+pos[1]
				if y < 20:
					cell = self.grid[x][y]
					cell['color'] = self.piece['color']
		return can_move
		
	def rotate(self):
		last_rotation = self.piece['rotation']
		self.piece['rotation'] = (self.piece['rotation'] + 1) % len(self.piece['piece_array'])
		pos_offset = None
		for pos_offset in ((0, 0), (1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)):
			can_rotate = True
			size = len(self.piece['piece_array'][0][0])
			for j in range(size):
				for i in range(size):
					if self.piece['piece_array'][self.piece['rotation']][size-j-1][i] != '.' and can_rotate:
						x, y = i+pos_offset[0]+self.piece['pos'][0], j+pos_offset[1]+self.piece['pos'][1]
						if y < 20:
							if x >= 0 and x < 10 and y >= 0:
								if not self.grid[x][y]['empty']:
									can_rotate = False
							else:
								can_rotate = False
			if can_rotate: break
		if can_rotate:
			for pos in self.piece['cells']:
				x, y = self.piece['pos'][0]+pos[0], self.piece['pos'][1]+pos[1]
				if y < 20:
					cell = self.grid[x][y]
					cell['color'] = (0.2, 0.2, 0.2)
			self.piece['cells'] = []
			self.piece['pos'][0] += pos_offset[0]
			self.piece['pos'][1] += pos_offset[1]
			size = len(self.piece['piece_array'][0][0])
			for j in range(size):
				for i in range(size):
					if self.piece['piece_array'][self.piece['rotation']][size-j-1][i] != '.':
						self.piece['cells'].append((i, j))
						x, y = self.piece['pos'][0]+i, self.piece['pos'][1]+j
						if y < 20:
							self.grid[x][y]['color'] = self.piece['color']
		else:
			self.piece['rotation'] = last_rotation		
					
	def up(self):
		while True:
			if self.down():
				break
			
	def down(self):
		self.tick_cooldown = 0
		if not self.move_piece(0, -1):
			for pos in self.piece['cells']:
				x, y = self.piece['pos'][0]+pos[0], self.piece['pos'][1]+pos[1]
				if y < 20:
					self.grid[x][y]['empty'] = False
				else:
					self.game_over = True
			if not self.game_over:
				y = 0
				lines_cleared = 0
				while y < 20:
					line_filled = True
					for x in range(10):
						if self.grid[x][y]['empty']:
							line_filled = False
							break
					if line_filled:
						for x in range(10):
							self.grid[x][y]['empty'] = True
							self.grid[x][y]['color'] = (0.2, 0.2, 0.2)
						lines_cleared += 1
						self.lines += 1
						if lines_cleared % 10 == 0:
							self.level += 1
							self.set_speed()
						for j in range(y, 20-1):
							for x in range(10):
								self.grid[x][j]['empty'] = self.grid[x][j+1]['empty']
								self.grid[x][j]['color'] = self.grid[x][j+1]['color']
						for x in range(10):
							self.grid[x][20-1]['empty'] = True
							self.grid[x][20-1]['empty'] = (0.2, 0.2, 0.2)
					else:
						y += 1
				if lines_cleared > 0:
					self.score += (40,100,300,1200)[lines_cleared-1]*(self.level+1)
				self.spawn_piece()
			return True
		else : return False
		
	def left(self):
		self.move_piece(-1, 0)
			
	def right(self):
		self.move_piece(1, 0)
			
	def update(self):
		if not self.game_over: self.tick_cooldown += 1
		if self.tick_cooldown >= self.tick_speed:
			self.down()
