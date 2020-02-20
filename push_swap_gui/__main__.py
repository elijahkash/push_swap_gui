#!/usr/bin/env python3

import tkinter as tk

from . import app_gui


def main():
	master = tk.Tk()
	app_gui.PushSwapGUI(master)
	try:
		master.mainloop()
	except KeyboardInterrupt:
		exit(0)
	exit(0)


if __name__ == '__main__':
	main()
