from utils import (
	DBG_HEIGHT,
	COLOR_WHITE,
	COLOR_GREY,
	COLOR_DBG_WHITE,
	COLOR_DBG_GREY
)
from pygame import font, Rect, display
from disassembler import dsm


class Debugger(object):
	def __init__(self, screen):
		self.scr = screen
		self.scr.height = self.scr.window_h
		self.dbg_h = DBG_HEIGHT * self.scr.sf
		self.scr.window_h += self.dbg_h

		self.reg_x = self.scr.window_w // 28
		self.var_x = self.scr.window_w // 4.6
		self.dsm_x = self.scr.window_w // 2.5
		self.y = self.scr.height * 1.05
		self.line_gap = self.scr.window_h // 33

		font.init()
		font_size = self.scr.sf * 1.6
		self.font = font.Font("font", int(font_size))

	def init_dbg(self, mem):
		self.mem = mem
		self.scr.surface.fill(
			COLOR_DBG_GREY, (0, 0, self.scr.window_w, self.scr.window_h)
		)
		self.init_buttons()
		display.flip()

	def draw_dbg(self, dbg_log):
		V = dbg_log["V"]
		PC = dbg_log["PC"]
		I = dbg_log["I"]
		dt = dbg_log["dt"]
		st = dbg_log["st"]

		self.scr.surface.fill(
			COLOR_DBG_GREY, (
				0,
				self.scr.height,
				self.scr.window_w,
				self.scr.window_h - self.scr.height - (self.scr.window_h//18)
			)
		)

		for i in range(16):
			self.draw_text(f"V{i:X}:{V[i]:X}", self.reg_x, self.y + (i*self.line_gap))

		self.draw_text(f"PC:{PC:X}", self.var_x, self.y)
		self.draw_text(f"I:{I:X}", self.var_x, self.y + self.line_gap)
		self.draw_text(f"DT:{dt:X}", self.var_x, self.y + (2*self.line_gap))
		self.draw_text(f"ST:{st:X}", self.var_x, self.y + (3*self.line_gap))

		try:
			dsm_op = self.dsm_code(PC)
		except IndexError:
			return

		for i in range(16):
			if dsm_op[i][0] == ">":
				self.draw_text(
					dsm_op[i], self.dsm_x, self.y + (i*self.line_gap), COLOR_DBG_WHITE
				)
			else:
				self.draw_text(
					dsm_op[i], self.dsm_x, self.y + (i*self.line_gap), COLOR_WHITE
				)

		display.flip()

	def draw_text(self, text, x, y, color=COLOR_WHITE):
		self.scr.surface.blit(self.font.render(text, False, color), (x, y))

	def dsm_code(self, PC):
		dsm_op = []

		for i in range(-16, 15, 2):
			mark = " "
			if i == 0:
				mark = ">"
			op = self.mem[PC + i] << 8 | self.mem[PC + i + 1]
			dsm_op.append(f"{mark}{PC + i:X} {op:04X} {dsm(op)}")

		return dsm_op

	def init_buttons(self):
		w = self.scr.window_w // 6.3
		h = self.scr.window_h // 28
		y = self.scr.window_h // 1.05
		total = 4
		gap = (self.scr.window_w - (total*w)) // (total+1)

		self.pause_button = self.draw_button(
			"PAUSE", gap, y, w, h, 1.3
		)
		self.step_button = self.draw_button(
			"STEP", (2*gap) + w, y, w, h, 1.11
		)
		self.resume_button = self.draw_button(
			"RESUME", (3*gap) + (2*w), y, w, h, 1.015
		)
		self.reset_button = self.draw_button(
			"RESET", (4*gap) + (3*w), y, w, h, 1.03
		)

	def draw_button(self, name, x, y, w, h, text_x_fac):
		button = self.scr.surface.fill(COLOR_WHITE, Rect((x, y, w, h)))
		self.draw_text(name, x * text_x_fac, y // 0.992, COLOR_GREY)
		return button
