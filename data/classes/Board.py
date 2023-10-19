import pygame
import sys
sys.path.insert(1, r'C:\Code\pythoncode-tutorials\gui-programming\chess-game\data\classes\ai')
from fetch_move import *
import fetch_move
from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn


# Game state checker
class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tile_width = width // 8
		self.tile_height = height // 8
		self.selected_piece = None
		self.turn = 'white'
		self.x = 0
		self.y = 0
		self.moves = []
		self.counter = 0
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'datanexus-397521-57a5a62691c0.json'
		self.movesb = []

		# try making it chess.board.fen()
		self.config = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
		]

		self.squares = self.generate_squares()

		self.setup_board()
	def state(self):
		state = self.turn
		print(state)
		if len(self.moves) > 4:
			self.moves = [self.moves[4],self.moves[5],self.moves[6],self.moves[7]]
		if state == 'white':
			self.counter = self.counter + 1
		if state == 'black':
			if self.counter < 1:
				result = fetch.fetch_move1(self.moves[0],self.moves[1],self.moves[2],self.moves[3],'pawn')
			if self.counter >= 1:
				result = fetch.fetch_move2(self.moves[0],self.moves[1],self.moves[2],self.moves[3],'pawn')
			self.moves.clear()
			if self.counter < 1:
				self.handle_click(result[0],result[1])
				self.handle_click(result[2],result[3])
			if self.counter >= 1:
				self.handle_click(result[0],result[1])
				self.handle_click(result[2],result[3])
		return state

	def generate_squares(self):
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(x,  y, self.tile_width, self.tile_height)
				)
		return output


	def get_square_from_pos(self, pos):
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square


	def get_piece_from_pos(self, pos):
		return self.get_square_from_pos(pos).occupying_piece


	def setup_board(self):
		# iterating 2d list
		for y, row in enumerate(self.config):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.get_square_from_pos((x, y))

					# looking inside contents, what piece does it have
					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					# as you notice above, we put `self` as argument, or means our class Board

					elif piece[1] == 'N':
						square.occupying_piece = Knight(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'B':
						square.occupying_piece = Bishop(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'Q':
						square.occupying_piece = Queen(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'K':
						square.occupying_piece = King(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'P':
						square.occupying_piece = Pawn(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)


	def handle_click(self, mx, my):
		if self.turn == 'white':
			x = mx // self.tile_width
			y = my // self.tile_height
		else: 
			x = mx
			y = my
		clicked_square = self.get_square_from_pos((x, y))
		print(x,y)
		self.x = x
		self.y = y
		if self.turn == 'white':
			self.moves.append(self.x)
			self.moves.append(self.y)
			print('my moves are', self.moves)
			self.movesb.clear()
			
		if self.turn == 'black':
			self.movesb.append(self.x)
			self.movesb.append(self.y)
			print('ai moves are', self.movesb)
			if len(self.moves) == 4:
				self.moves.clear()
		if self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece
					print('oh')
		elif self.selected_piece.move(self, clicked_square):
			self.turn = 'white' if self.turn == 'black' else 'black'
			print('hi')
			self.state()
		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == self.turn:
				self.selected_piece = clicked_square.occupying_piece
				print('no')

	def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
		output = False
		king_pos = None

		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.occupying_piece
					old_square = square
					old_square.occupying_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.occupying_piece
					new_square.occupying_piece = changing_piece

		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K' and piece.color == color:
						king_pos = piece.pos
		for piece in pieces:
			if piece.color != color:
				for square in piece.attacking_squares(self):
					if square.pos == king_pos:
						output = True

		if board_change is not None:
			old_square.occupying_piece = changing_piece
			new_square.occupying_piece = new_square_old_piece
						
		return output


	def is_in_checkmate(self, color):
		output = False

		for piece in [i.occupying_piece for i in self.squares]:
			if piece != None:
				if piece.notation == 'K' and piece.color == color:
					king = piece

		if king.get_valid_moves(self) == []:
			if self.is_in_check(color):
				output = True

		return output


	def draw(self, display):
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)