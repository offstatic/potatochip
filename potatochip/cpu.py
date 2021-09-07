from utils import (
	SCREEN_WIDTH_LORES,
	SCREEN_HEIGHT_LORES,
	SCREEN_WIDTH_HIRES,
	SCREEN_HEIGHT_HIRES,
	PC_OFFSET
)
from random import randint
from time import time
import sys


class CPU(object):
	def __init__(self, speed=600):
		self.speed = speed // 60

	def reset(self):
		self.screen_w = SCREEN_WIDTH_LORES
		self.screen_h = SCREEN_HEIGHT_LORES
		self.draw_flag = False
		self.cycle_count = 0
		self.last_time = time()
		self.hires_mode = False

		self.mem = [0] * 4096
		self.video_mem = [0] * self.screen_w * self.screen_h
		self.V = [0] * 16
		self.I = 0
		self.PC = PC_OFFSET
		self.dt = 0
		self.st = 0
		self.stack = []
		self.key = [0] * 16
		self.flag = [0] * 16

	def load_rom(self, path, offset=PC_OFFSET, is_bin=True):
		if is_bin:
			with open(path, "rb") as f:
				byte_array = f.read()
		else:
			byte_array = path

		for i, byte in enumerate(byte_array):
			self.mem[offset + i] = byte

	def get_video_mem(self):
		return self.video_mem

	def set_key(self, key, value):
		self.key[key] = value

	def get_mode(self):
		return self.hires_mode

	def cycle(self):
		"""CPU speed is based on cycles per 1/60 sec"""
		if self.cycle_count < self.speed:
			op = self.mem[self.PC] << 8 | self.mem[self.PC + 1]
			self.PC += 2

			self.nibble = (op & 0xF000) >> 12
			self.X = (op & 0x0F00) >> 8
			self.Y = (op & 0x00F0) >> 4
			self.N = op & 0x000F
			self.NN = op & 0x00FF
			self.NNN = op & 0x0FFF

			try:
				self.op_lookup()
			except Exception:
				print("Error in", hex(op))

			self.cycle_count += 1

		if time() - self.last_time >= 1/60:
			if self.dt > 0:
				self.dt -= 1
			if self.st > 0:
				self.st -= 1
			self.cycle_count = 0
			self.last_time = time()

	def op_lookup(self):
		op_0_map = {
			0x0C: self.op_00CN,             # SCD
			0xE0: self.op_00E0,             # CLS
			0xEE: self.op_00EE,             # RET
			0xFB: self.op_00FB,             # SCR
			0xFC: self.op_00FC,             # SCL
			0xFD: self.op_00FD,             # EXIT
			0xFE: self.op_00FE,             # LOW
			0xFF: self.op_00FF              # HIGH
		}

		op_8_map = {
			0x0: self.op_8XY0,              # LD
			0x1: self.op_8XY1,              # OR
			0x2: self.op_8XY2,              # AND
			0x3: self.op_8XY3,              # XOR
			0x4: self.op_8XY4,              # ADD
			0x5: self.op_8XY5,              # SUB
			0x6: self.op_8XY6,              # SHR
			0x7: self.op_8XY7,              # SUBN
			0xE: self.op_8XYE               # SHL
		}

		op_E_map = {
			0x9E: self.op_EX9E,             # SKP
			0xA1: self.op_EXA1              # SKNP
		}

		op_F_map = {
			0x07: self.op_FX07,             # LD
			0x0A: self.op_FX0A,             # LD
			0x15: self.op_FX15,             # LD
			0x18: self.op_FX18,             # LD
			0x1E: self.op_FX1E,             # ADD
			0x29: self.op_FX29,             # LD
			0x30: self.op_FX30,             # LD
			0x33: self.op_FX33,             # LD
			0x55: self.op_FX55,             # LD
			0x65: self.op_FX65,             # LD
			0x75: self.op_FX75,             # LD
			0x85: self.op_FX85              # LD
		}

		op_misc_map = {
			0x1: self.op_1NNN,              # JP
			0x2: self.op_2NNN,              # CALL
			0x3: self.op_3XNN,              # SE
			0x4: self.op_4XNN,              # SNE
			0x5: self.op_5XY0,              # SE
			0x6: self.op_6XNN,              # LD
			0x7: self.op_7XNN,              # ADD
			0x9: self.op_9XY0,              # SNE
			0xA: self.op_ANNN,              # LD
			0xB: self.op_BNNN,              # JP
			0xC: self.op_CXNN,              # RND
			0xD: self.op_DXYN               # DRW
		}

		if self.nibble == 0x0:
			if self.Y == 0xC:
				op_0_map[self.Y]()
			else:
				op_0_map[self.NN]()
		elif self.nibble == 0x8:
			op_8_map[self.N]()
		elif self.nibble == 0xE:
			op_E_map[self.NN]()
		elif self.nibble == 0xF:
			op_F_map[self.NN]()
		else:
			op_misc_map[self.nibble]()

###########################################################
# Opcodes
###########################################################

	def op_00CN(self):
		# Scroll down by N pixels
		for r in range((self.screen_h-1) - self.N, -1, -1):
			for c in range(self.screen_w):
				self.video_mem[(self.screen_w * (r+self.N)) + c] = \
					self.video_mem[(self.screen_w*r) + c]

		# Fill the top N rows with blank pixels
		for r in range(self.N):
			for c in range(self.screen_w):
				self.video_mem[(self.screen_w*r) + c] = 0

		self.draw_flag = True

	def op_00E0(self):
		self.video_mem = [0] * self.screen_w * self.screen_h
		self.draw_flag = True

	def op_00EE(self):
		self.PC = self.stack.pop()

	def op_00FB(self):
		# Scroll right by 4 pixels
		for r in range((self.screen_w-1) - 4, -1, -1):
			for c in range(self.screen_h):
				self.video_mem[((self.screen_w*c) + 4) + r] = \
					self.video_mem[(self.screen_w*c) + r]

		# Fill the left 4 columns with blank pixels
		for r in range(self.screen_h):
			for c in range(4):
				self.video_mem[(self.screen_w*r) + c] = 0

		self.draw_flag = True

	def op_00FC(self):
		# Scroll left by 4 pixels
		for r in range(4, self.screen_w):
			for c in range(self.screen_h):
				self.video_mem[((self.screen_w*c) - 4) + r] = \
					self.video_mem[(self.screen_w*c) + r]

		# Fill the right 4 columns with blank pixels
		for r in range(self.screen_h):
			for c in range(self.screen_w - 1, self.screen_w - 4 - 1, -1):
				self.video_mem[(self.screen_w*r) + c] = 0

		self.draw_flag = True

	def op_00FD(self):
		sys.exit()

	def op_00FE(self):
		self.screen_w = SCREEN_WIDTH_LORES
		self.screen_h = SCREEN_HEIGHT_LORES
		self.video_mem = [0] * self.screen_w * self.screen_h
		self.hires_mode = False

	def op_00FF(self):
		self.screen_w = SCREEN_WIDTH_HIRES
		self.screen_h = SCREEN_HEIGHT_HIRES
		self.video_mem = [0] * self.screen_w * self.screen_h
		self.hires_mode = True

	def op_1NNN(self):
		self.PC = self.NNN

	def op_2NNN(self):
		self.stack.append(self.PC)
		self.PC = self.NNN

	def op_3XNN(self):
		if self.V[self.X] == self.NN:
			self.PC += 2

	def op_4XNN(self):
		if self.V[self.X] != self.NN:
			self.PC += 2

	def op_5XY0(self):
		if self.V[self.X] == self.V[self.Y]:
			self.PC += 2

	def op_6XNN(self):
		self.V[self.X] = self.NN

	def op_7XNN(self):
		self.V[self.X] = (self.V[self.X] + self.NN) & 0xFF

	def op_8XY0(self):
		self.V[self.X] = self.V[self.Y]

	def op_8XY1(self):
		self.V[self.X] |= self.V[self.Y]

	def op_8XY2(self):
		self.V[self.X] &= self.V[self.Y]

	def op_8XY3(self):
		self.V[self.X] ^= self.V[self.Y]

	def op_8XY4(self):
		temp = self.V[self.X] + self.V[self.Y]
		self.V[self.X] = temp & 0xFF
		self.V[0xF] = 1 if (temp > 0xFF) else 0

	def op_8XY5(self):
		self.V[0xF] = 1 if (self.V[self.X] >= self.V[self.Y]) else 0
		self.V[self.X] = self.V[self.X] - self.V[self.Y] & 0xFF

	def op_8XY6(self):
		self.V[0xF] = 1 if (self.V[self.X] & 0x1) else 0
		self.V[self.X] = (self.V[self.X] >> 1) & 0xFF

	def op_8XY7(self):
		self.V[0xF] = 1 if (self.V[self.Y] >= self.V[self.X]) else 0
		self.V[self.X] = (self.V[self.Y] - self.V[self.X]) & 0xFF

	def op_8XYE(self):
		self.V[0xF] = 1 if ((self.V[self.X] >> 7) & 0x01) else 0
		self.V[self.X] = (self.V[self.X] << 1) & 0xFF

	def op_9XY0(self):
		if self.V[self.X] != self.V[self.Y]:
			self.PC += 2

	def op_ANNN(self):
		self.I = self.NNN

	def op_BNNN(self):
		self.PC = self.NNN + self.V[0x0]

	def op_CXNN(self):
		self.V[self.X] = randint(0, 255) & self.NN

	def op_DXYN(self):
		x_pos = self.V[self.X]
		y_pos = self.V[self.Y]
		self.V[0xF] = 0
		if self.N == 0:
			half_sprite = self.I
			sprite_h = 16
			sprite_l = 16
			bit_checker = 0x8000
		else:
			sprite = self.mem[self.I: self.I + self.N]
			sprite_h = len(sprite)
			sprite_l = 8
			bit_checker = 0x80

		for y_sprite in range(sprite_h):
			if self.N == 0:
				# Each 2 byte schip sprite row is loaded in two halves
				byte = (self.mem[half_sprite] << 8) | self.mem[half_sprite + 1]
				half_sprite += 2
			else:
				byte = sprite[y_sprite]
			y_coord = ((y_pos+y_sprite) % self.screen_h) * self.screen_w
			if y_coord >= self.screen_h * self.screen_w:
				continue

			for x_sprite in range(sprite_l):
				x_coord = (x_pos+x_sprite) % self.screen_w
				if x_coord >= self.screen_w:
					continue
				# Check sprite bits for non-zero
				# then flip the pixel bits by XORing
				if (byte & (bit_checker >> x_sprite)) != 0:
					if self.video_mem[x_coord + y_coord] == 1:
						self.V[0xF] = 1
					self.video_mem[x_coord + y_coord] ^= 1

		self.draw_flag = True

	def op_EX9E(self):
		if self.key[self.V[self.X]] == 1:
			self.PC += 2

	def op_EXA1(self):
		if self.key[self.V[self.X]] != 1:
			self.PC += 2

	def op_FX07(self):
		self.V[self.X] = self.dt

	def op_FX0A(self):
		self.PC -= 2

		for k in range(16):
			if self.key[k] == 1:
				self.V[self.X] = k
				self.PC += 2
				break

	def op_FX15(self):
		self.dt = self.V[self.X]

	def op_FX18(self):
		self.st = self.V[self.X]

	def op_FX1E(self):
		self.I += self.V[self.X]

	def op_FX29(self):
		self.I = 5 * self.V[self.X]

	def op_FX30(self):
		"""Schip fonts are stored from memloc 0x50"""
		self.I = (10*self.V[self.X]) + 0x50

	def op_FX33(self):
		self.mem[self.I] = self.V[self.X] // 100
		self.mem[self.I + 1] = (self.V[self.X] % 100) // 10
		self.mem[self.I + 2] = self.V[self.X] % 10

	def op_FX55(self):
		for i in range(self.X + 1):
			self.mem[self.I + i] = self.V[i]

	def op_FX65(self):
		for i in range(self.X + 1):
			self.V[i] = self.mem[self.I + i]

	def op_FX75(self):
		for i in range(self.X + 1):
			self.flag[i] = self.V[i]

	def op_FX85(self):
		for i in range(self.X + 1):
			self.V[i] = self.flag[i]
