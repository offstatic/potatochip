from utils import (
	SCREEN_WIDTH_LORES,
	SCREEN_HEIGHT_LORES,
	COLOR_WHITE,
	COLOR_GREY
)
from pygame import display, Rect

PIXEL_SIZE = 10


class Screen(object):
	def __init__(self, scale_factor):
		self.sf = int(scale_factor * PIXEL_SIZE)
		self.window_w = SCREEN_WIDTH_LORES * self.sf
		self.window_h = SCREEN_HEIGHT_LORES * self.sf

	def init_screen(self):
		display.init()
		self.surface = display.set_mode((self.window_w, self.window_h))

	def draw(self, video_mem):
		for pos in range(len(video_mem)):
			if video_mem[pos] == 1:
				color = COLOR_WHITE
			else:
				color = COLOR_GREY
			x = (pos % SCREEN_WIDTH_LORES) * self.sf
			y = (pos // SCREEN_WIDTH_LORES) * self.sf
			self.surface.fill(color, Rect(x, y, self.sf, self.sf))

		display.flip()
