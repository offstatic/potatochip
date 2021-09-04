from cpu import CPU
from screen import Screen
import pygame
import sys


class Emulator(object):
	def __init__(self, arg):
		self.arg = arg
		self.cpu = CPU(self.arg.speed)
		self.scr = Screen(self.arg.scale)
		self.init()

		self.keymap = {
			pygame.K_1: 0x1,
			pygame.K_2: 0x2,
			pygame.K_3: 0x3,
			pygame.K_4: 0xC,
			pygame.K_q: 0x4,
			pygame.K_w: 0x5,
			pygame.K_e: 0x6,
			pygame.K_r: 0xD,
			pygame.K_a: 0x7,
			pygame.K_s: 0x8,
			pygame.K_d: 0x9,
			pygame.K_f: 0xE,
			pygame.K_z: 0xA,
			pygame.K_x: 0x0,
			pygame.K_c: 0xB,
			pygame.K_v: 0xF
		}

	def init(self):
		self.cpu.reset()

		try:
			self.cpu.load_rom(self.arg.ROM)
		except FileNotFoundError:
			print("Invalid file")
			sys.exit

		# Create window after a valid file is loaded in memory
		self.scr.init_screen()

	def run(self):
		running = True

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.KEYDOWN:
					if event.key in self.keymap:
						self.cpu.set_key(self.keymap[event.key], 1)
				if event.type == pygame.KEYUP:
					if event.key in self.keymap:
						self.cpu.set_key(self.keymap[event.key], 0)
			self.step()

	def step(self):
		self.cpu.cycle()
		if self.cpu.draw_flag:
			self.scr.draw(self.cpu.get_video_mem())
			self.cpu.draw_flag = False
