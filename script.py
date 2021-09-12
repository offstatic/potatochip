import psp2d
from cpu import CPU
from utils import (
	SCREEN_WIDTH_LORES,
	SCREEN_WIDTH_HIRES,
	PC_OFFSET,
	COLOR_WHITE,
	COLOR_GREY,
	CHIP_FONT,
	OCTO_FONT
)

PIXEL_SIZE = 7
WR, WG, WB = COLOR_WHITE
GR, GG, GB = COLOR_GREY


def main():
	block = psp2d.Image(PIXEL_SIZE, PIXEL_SIZE)
	surface = psp2d.Screen()
	cpu = CPU(600)
	cpu.reset()
	load_rom(cpu, CHIP_FONT, 0x0, False)
	load_rom(cpu, OCTO_FONT, 0x50, False)
	load_rom(cpu, "ROM")

	while True:
		cpu.cycle()
		if cpu.draw_flag:
			draw(cpu.get_video_mem(), block, surface, cpu.get_mode())
			cpu.draw_flag = False

		pad = psp2d.Controller()
		if pad.cross:
			break


def load_rom(cpu, path, offset=PC_OFFSET, is_bin=True):
	if is_bin:
		f = open(path, "rb")
		try:
			for i, byte in enumerate(f.read()):
				cpu.mem[offset + i] = ord(byte)
		finally:
			f.close()
	else:
		for i, byte in enumerate(path):
			cpu.mem[offset + i] = byte


def draw(video_mem, block, surface, hires_mode):
	for pos in range(len(video_mem)):
		if video_mem[pos] == 1:
			color = psp2d.Color(WR, WG, WB)
		else:
			color = psp2d.Color(GR, GG, GB)

		if hires_mode:
			x = ((pos % SCREEN_WIDTH_HIRES) * PIXEL_SIZE) // 2
			y = ((pos // SCREEN_WIDTH_HIRES) * PIXEL_SIZE) // 2
		else:
			x = (pos % SCREEN_WIDTH_LORES) * PIXEL_SIZE
			y = (pos // SCREEN_WIDTH_LORES) * PIXEL_SIZE

		block.clear(color)
		surface.blit(block, dx=x, dy=y)

	surface.swap()


if __name__ == "__main__":
	main()
