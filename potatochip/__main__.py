from emulator import Emulator
import argparse


def main():
	emulator = Emulator(args())
	emulator.run()


def args():
	parser = argparse.ArgumentParser(
		description="Run Chip8 roms"
	)
	parser.add_argument("ROM", help="ROM file")
	parser.add_argument(
		"--speed", dest="speed", default=600,
		type=int, help="Emulator speed"
	)
	parser.add_argument(
		"--scale", dest="scale", default=1,
		type=float, help="Window size"
	)
	return parser.parse_args()


if __name__ == "__main__":
	main()
