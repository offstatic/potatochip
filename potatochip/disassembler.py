def dsm(op):
	_00FF = op & 0x00FF
	_F000 = op & 0xF000
	_F00F = op & 0xF00F
	_F0FF = op & 0xF0FF
	_FFF0 = op & 0xFFF0

	X = (op & 0x0F00) >> 8
	Y = (op & 0x00F0) >> 4
	N = op & 0x000F
	NN = op & 0x000F
	NNN = op & 0x0FFF

	# Misc
	if _F000 == 0x1000:
		return f"JP {NNN:X}"
	elif _F000 == 0x2000:
		return f"CALL {NNN:X}"
	elif _F000 == 0x3000:
		return f"SE V{X:X}, {NN:X}"
	elif _F000 == 0x4000:
		return f"SNE V{X:X}, {NN:X}"
	elif _F000 == 0x5000:
		return f"SE V{X:X}, V{Y:X}"
	elif _F000 == 0x6000:
		return f"LD V{X:X}, {NN:X}"
	elif _F000 == 0x7000:
		return f"ADD V{X:X}, {NN:X}"
	elif _F000 == 0x9000:
		return f"SNE V{X:X}, V{Y:X}"
	elif _F000 == 0xA000:
		return f"LD I, {NNN:X}"
	elif _F000 == 0xB000:
		return f"LD V0, {NNN:X}"
	elif _F000 == 0xC000:
		return f"RND V{X:X}, {NN:X}"
	elif _F000 == 0xD000:
		return f"DRW V{X:X}, V{Y:X}, {N:X}"
	# 8
	elif _F00F == 0x8000:
		return f"LD V{X:X}, V{Y:X}"
	elif _F00F == 0x8001:
		return f"OR V{X:X}, V{Y:X}"
	elif _F00F == 0x8002:
		return f"AND V{X:X}, V{Y:X}"
	elif _F00F == 0x8003:
		return f"XOR V{X:X}, V{Y:X}"
	elif _F00F == 0x8004:
		return f"ADD V{X:X}, V{Y:X}"
	elif _F00F == 0x8005:
		return f"SUB V{X:X}, V{Y:X}"
	elif _F00F == 0x8006:
		return f"SHR V{X:X} {{, V{Y:X}}}"
	elif _F00F == 0x8007:
		return f"SUBN V{X:X}, V{Y:X}"
	elif _F00F == 0x800E:
		return f"SHL V{X:X} {{, V{Y:X}}}"
	# E
	elif _F0FF == 0xE09E:
		return f"SKP V{X:X}"
	elif _F0FF == 0xE0A1:
		return f"SKNP V{X:X}"
	# F
	elif _F0FF == 0xF007:
		return f"LD V{X:X}, DT"
	elif _F0FF == 0xF00A:
		return f"LD V{X:X}, K"
	elif _F0FF == 0xF015:
		return f"LD DT, V{X:X}"
	elif _F0FF == 0xF018:
		return f"LD ST, V{X:X}"
	elif _F0FF == 0xF01E:
		return f"ADD I, V{X:X}"
	elif _F0FF == 0xF029:
		return f"LD F, V{X:X}"
	elif _F0FF == 0xF030:
		return f"LD HF, V{X:X}"
	elif _F0FF == 0xF033:
		return f"LD B, V{X:X}"
	elif _F0FF == 0xF055:
		return f"LD [I],  V{X:X}"
	elif _F0FF == 0xF065:
		return f"LD V{X:X}, [I]"
	elif _F0FF == 0xF075:
		return f"LD R, V{X:X}"
	elif _F0FF == 0xF085:
		return f"LD V{X:X}, R"
	# 0
	elif _FFF0 == 0x00C0:
		return f"SCD {N:X}"
	elif _00FF == 0x00E0:
		return "CLS"
	elif _00FF == 0x00EE:
		return "RET"
	elif _00FF == 0x00FB:
		return "SCR"
	elif _00FF == 0x00FC:
		return "SCL"
	elif _00FF == 0x00FD:
		return "EXIT"
	elif _00FF == 0x00FE:
		return "LOW"
	elif _00FF == 0x00FF:
		return "HIGH"
	else:
		return " "
