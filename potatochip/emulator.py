from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from cpu import CPU
from screen import Screen
from utils import CHIP_FONT, OCTO_FONT
from debugger import Debugger
from pathlib import Path
import fontgen
import pygame
import sys


class Emulator(object):
	def __init__(self, arg):
		self.arg = arg
		self.cpu = CPU(self.arg.speed)
		self.scr = Screen(self.arg.scale)
		if self.arg.dbg:
			if not Path("font").is_file():
				fontgen.generate()
			self.dbg = Debugger(self.scr)
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

	def init(self, reset=False):
		self.cpu.reset()
		self.cpu.load_rom(CHIP_FONT, 0x0, False)
		self.cpu.load_rom(OCTO_FONT, 0x50, False)

		try:
			self.cpu.load_rom(self.arg.ROM)
		except FileNotFoundError:
			print("Invalid file")
			sys.exit

		# Create window after a valid file is loaded in memory
		if not reset:
			self.scr.init_screen(f"PotatoChip - {Path(self.arg.ROM).name}")
		if self.arg.dbg:
			self.dbg.init_dbg(self.cpu.get_mem())
			self.dbg.draw_dbg(self.cpu.dbg_log())
		self.scr.draw(self.cpu.get_video_mem(), self.cpu.get_mode())

	def run(self):
		running = True
		self.paused = False

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.KEYDOWN:
					if event.key in self.keymap:
						self.cpu.set_key(self.keymap[event.key], 1)
					if event.key == pygame.K_SPACE:
						self.paused = not self.paused
					if event.key == pygame.K_n:
						self.step()
					if event.key == pygame.K_ESCAPE:
						self.init(True)

				if event.type == pygame.KEYUP:
					if event.key in self.keymap:
						self.cpu.set_key(self.keymap[event.key], 0)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pygame.mouse.get_pos()
					if self.dbg.pause_button.collidepoint(mouse_pos):
						self.paused = True
					if self.dbg.step_button.collidepoint(mouse_pos):
						self.step()
					if self.dbg.resume_button.collidepoint(mouse_pos):
						self.paused = False
					if self.dbg.reset_button.collidepoint(mouse_pos):
						self.init(True)

			if not self.paused:
				self.step()

	def step(self):
		try:
			self.cpu.cycle()
		except IndexError:
			self.paused = True
			print("Error in rom, execution paused")
		if self.cpu.draw_flag:
			self.scr.draw(self.cpu.get_video_mem(), self.cpu.get_mode())
			self.cpu.draw_flag = False
		if self.arg.dbg:
			self.dbg.draw_dbg(self.cpu.dbg_log())
