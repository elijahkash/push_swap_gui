#!/usr/bin/env python3

import tkinter as tk

import push_swap_gui


def main():
	master = tk.Tk()
	push_swap_gui.PushSwapGUI(master)
	try:
		master.mainloop()
	except KeyboardInterrupt:
		exit(0)
	return 0


if __name__ == '__main__':
	exit(main())
