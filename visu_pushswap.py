#!/usr/bin/env python3

# visualizer for push-swap project

import random as rand
import time
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import ttk
import collections as coll
import subprocess
from colour import Color

# TODO: depend from display?
DEFAULT_WIN_SIZE_X = 1000
DEFAULT_WIN_SIZE_Y = 1000
WIN_TITLE = 'py_push-swap'

DEFAULT_RANGE_A = 0
DEFAULT_RANGE_B = 100

COLOR_START = "limegreen"
COLOR_END = "orangered"

SPEED_DELTA = 1.5


class PushSwapStacks:
	"""
	describe stacks for push-swap algorithm
	"""

	def __init__(self, initstate):
		""" initstate: Iterable[_T]=..."""
		self.stack_a = coll.deque()
		self.stack_b = coll.deque()
		self.new_data(initstate)
		self.cmd = {
			'pa': self.pa,
			'pb': self.pb,
			'sa': self.sa,
			'sb': self.sb,
			'ss': self.ss,
			'ra': self.ra,
			'rb': self.rb,
			'rr': self.rr,
			'rra': self.rra,
			'rrb': self.rrb,
			'rrr': self.rrr
		}

	def new_data(self, initstate):
		self.stack_a.clear()
		self.stack_b.clear()
		tmp = sorted(initstate)
		self.stack_a.extend([tmp.index(x) + 1 for x in initstate])

	def pa(self):
		if len(self.stack_b):
			self.stack_a.appendleft(self.stack_b.popleft())

	def pb(self):
		if len(self.stack_a):
			self.stack_b.appendleft(self.stack_a.popleft())

	def ra(self):
		if len(self.stack_a):
			self.stack_a.rotate(-1)

	def rb(self):
		if len(self.stack_b):
			self.stack_b.rotate(-1)

	def rr(self):
		self.ra()
		self.rb()

	def rra(self):
		if len(self.stack_a):
			self.stack_a.rotate(1)

	def rrb(self):
		if len(self.stack_b):
			self.stack_b.rotate(1)

	def rrr(self):
		self.rra()
		self.rrb()

	def sa(self):
		self.stack_a[0], self.stack_a[1] = self.stack_a[1], self.stack_a[0]

	def sb(self):
		self.stack_b[0], self.stack_b[1] = self.stack_b[1], self.stack_b[0]

	def ss(self):
		self.sa()
		self.sb()


class GameInfo:
	def __init__(self):
		self.src_data = []
		self.colors = []
		self.generate_data(DEFAULT_RANGE_A, DEFAULT_RANGE_B)
		self.st = PushSwapStacks(self.src_data)
		self.op_list = []
		self.cur_op = 0
		self.game = 0
		self.speed = 500
		self.op_count = 0
		self.stack_state = ''
		self.use_builtin = tk.IntVar()
		self.use_builtin.set(1)

	def reset(self):
		self.cur_op = 0
		self.game = 0
		self.st.new_data(self.src_data)

	def generate_data(self, a, b):
		self.src_data = [x for x in range(a, b)]
		rand.shuffle(self.src_data)
		self.colors = list(
			Color(COLOR_START).range_to(Color(COLOR_END), a - b)
		)

	def speed_up(self):
		self.speed = int(self.speed / SPEED_DELTA)

	def speed_down(self):
		self.speed = int(round(self.speed * SPEED_DELTA))
		if self.speed > 1000:
			self.speed = 1000
		elif self.speed == 0:
			self.speed = 1


class VisuPS(ttk.Frame):
	def __init__(self, root):
		super().__init__(master=root, padding="5 2 5 2")
		root.wm_resizable(False, False)
		root.geometry(f'{DEFAULT_WIN_SIZE_X}x{DEFAULT_WIN_SIZE_Y}+0+0')
		root.title(WIN_TITLE)
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		self.root = root
		self.style = ttk.Style()
		self.style.theme_use('aqua')
		self.grid(sticky=(tk.N, tk.W, tk.E, tk.S))
		self.game_info = GameInfo()
		self.__initUI()
		self.update()
		self.draw()

	def __initUI(self):
		self.canvas_a = tk.Canvas(self)
		self.canvas_b = tk.Canvas(self)
		self.cmd_list = scrolledtext.ScrolledText(
			self, width=5, state='disable'
		)
		self.menu_frame = ttk.Frame(self)
		self.quit_button = ttk.Button(
			self.menu_frame, text='Quit', command=self.visu_exit
		)
		self.start_button = ttk.Button(
			self.menu_frame, text='Calculate', command=self.start
		)
		self.speed_down_button = ttk.Button(
			self.menu_frame, text='<<', command=self.speed_down
		)
		self.speed_pause_button = ttk.Button(
			self.menu_frame, text='▷', command=self.game
		)
		self.speed_up_button = ttk.Button(
			self.menu_frame, text='>>', command=self.speed_up
		)
		self.reset_button = ttk.Button(
			self.menu_frame, text='Reset', command=self.reset
		)
		self.generate_new_data_button = ttk.Button(
			self.menu_frame, text='Generate new [a, b)',
			command=self.generate_new_data
		)
		self.entry_range_a = ttk.Entry(self.menu_frame, width=10)
		self.entry_range_a.insert(0, str(DEFAULT_RANGE_A))
		self.entry_range_b = ttk.Entry(self.menu_frame, width=10)
		self.entry_range_b.insert(0, str(DEFAULT_RANGE_B))
		self.entry_range_a_label = ttk.Label(self.menu_frame, text='<- input a')
		self.entry_range_b_label = ttk.Label(self.menu_frame, text='<- input b')
		self.use_builtin = ttk.Checkbutton(
			self.menu_frame, text='use built-in algo',
			command=self.builtin_click, variable=self.game_info.use_builtin
		)
		self.input_file_name = ttk.Label(
			self.menu_frame, text='Custom push_swap:'
		)
		self.push_swap_file_name = ttk.Entry(
			self.menu_frame, width=30, state=tk.DISABLED
		)
		self.open_file = ttk.Button(
			self.menu_frame, text='choose file ...', command=self.choose_file,
			state=tk.DISABLED
		)
		self.speed = ttk.Label(
			self.menu_frame,
			text=f'speed (delay between ops in msec): {self.game_info.speed}'
		)
		self.op_num = ttk.Label(
			self.menu_frame,
			text=f'operations count = {self.game_info.op_count}'
		)
		self.stack_state = ttk.Label(self.menu_frame, text='stack state:  ')
		self.powered_by = ttk.Label(
			self.menu_frame, text='powered by Ilya Kashnitkiy', anchor=tk.CENTER
		)
		self.git_link = ttk.Label(
			self.menu_frame, text='github.com/elijahkash', anchor=tk.CENTER
		)


		STICKY_FULL = {'sticky': (tk.W, tk.E, tk.N, tk.S)}
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=20)
		self.columnconfigure(2, weight=20)
		self.columnconfigure(3, weight=1)

		self.canvas_a.grid(column=1, row=0, pady=4, padx=2, **STICKY_FULL)
		self.canvas_b.grid(column=2, row=0, pady=4, padx=2, **STICKY_FULL)
		self.cmd_list.grid(column=3, row=0, pady=4, **STICKY_FULL)
		self.menu_frame.grid(column=0, row=0, pady=4, padx=4, **STICKY_FULL)

		for i in range(0, 3):
			self.menu_frame.columnconfigure(i, weight=1)
		for i in range(0, 90):
			self.menu_frame.rowconfigure(i, weight=1)

		self.quit_button.grid(row=0, columnspan=3, **STICKY_FULL)
		self.start_button.grid(row=1, columnspan=3, **STICKY_FULL)
		self.speed_down_button.grid(row=2, column=0, **STICKY_FULL)
		self.speed_pause_button.grid(row=2, column=1, **STICKY_FULL)
		self.speed_up_button.grid(row=2, column=2, **STICKY_FULL)
		self.reset_button.grid(row=3, columnspan=3, **STICKY_FULL)
		self.generate_new_data_button.grid(row=4, columnspan=3, **STICKY_FULL)
		self.entry_range_a.grid(row=5, column=0)
		self.entry_range_b.grid(row=6, column=0)
		self.entry_range_a_label.grid(row=5, column=2, **STICKY_FULL)
		self.entry_range_b_label.grid(row=6, column=2, **STICKY_FULL)
		self.use_builtin.grid(row=7, columnspan=3, **STICKY_FULL)
		self.input_file_name.grid(row=8, columnspan=3, **STICKY_FULL)
		self.push_swap_file_name.grid(
			in_=self.menu_frame, row=9, columnspan=3, **STICKY_FULL
		)
		self.open_file.grid(row=8, column=2, **STICKY_FULL)
		self.powered_by.grid(row=40, column=0, columnspan=3, **STICKY_FULL)
		self.git_link.grid(row=41, column=0, columnspan=3, **STICKY_FULL)
		self.speed.grid(row=13, column=0, columnspan=3, **STICKY_FULL)
		self.op_num.grid(row=14, column=0, columnspan=3, **STICKY_FULL)
		self.stack_state.grid(row=15, column=0, columnspan=3, **STICKY_FULL)

	def visu_exit(self):
		tk.Tk.quit(self.root)

	def choose_file(self):
		tmp = filedialog.askopenfilename()
		self.push_swap_file_name.delete(0, tk.END)
		self.push_swap_file_name.insert(0, tmp)

	def builtin_click(self):
		if self.game_info.use_builtin.get():
			self.open_file.config(state=tk.DISABLED)
			self.push_swap_file_name.config(state=tk.DISABLED)
		else:
			self.open_file.config(state=tk.NORMAL)
			self.push_swap_file_name.config(state=tk.NORMAL)

	def speed_up(self):
		self.game_info.speed_up()
		self.speed.config(
			text=f'speed (delay between ops in msec): {self.game_info.speed}'
		)

	def speed_down(self):
		self.game_info.speed_down()
		self.speed.config(
			text=f'speed (delay between ops in msec): {self.game_info.speed}'
		)

	def game(self):
		if self.game_info.game:
			self.game_info.game = 0
			self.speed_pause_button.config(text='▷')
		else:
			self.game_info.game = time.time()
			self.speed_pause_button.config(text='||')
			self.next_op(self.game_info.game)

	def next_op(self, id_value):
		if self.game_info.game != id_value:
			return
		if len(self.game_info.op_list) == self.game_info.cur_op:
			self.draw()
			self.update_status()
			self.game_info.game = 0
			self.speed_pause_button.config(text='▷')
			return
		self.game_info.st.cmd[self.game_info.op_list[self.game_info.cur_op]]()
		self.game_info.cur_op += 1
		if self.game_info.speed:
			self.draw()
		self.cmd_list.config(state='normal')
		self.cmd_list.insert(
			tk.END, self.game_info.op_list[self.game_info.cur_op - 1] + '\n'
		)
		self.cmd_list.yview(tk.END)
		self.cmd_list.config(state='disabled')
		if self.game_info.speed == 0 and self.game_info.cur_op % 128 == 0:
			self.draw()
			self.update()
		self.after(self.game_info.speed, self.next_op, id_value)

	def reset(self):
		self.game_info.reset()
		self.draw()
		self.speed_pause_button.config(text='▷')
		self.set_default_status()
		self.cmd_list.config(state='normal')
		self.cmd_list.delete(1.0, tk.END)
		self.cmd_list.config(state='disabled')

	def update_status(self):
		if len(self.game_info.src_data) == len(self.game_info.st.stack_a) and all(self.game_info.st.stack_a[i] < self.game_info.st.stack_a[i + 1] for i in range(len(self.game_info.src_data) - 1)):
			self.stack_state.config(
				text='stack state:  OK',
				foreground='green4'
			)
		else:
			self.stack_state.config(
				text='stack state:  KO',
				foreground='red2'
			)

	def set_default_status(self):
		self.stack_state.config(
			text='stack state:',
			foreground='black'
		)

	def generate_new_data(self):
		a = int(self.entry_range_a.get())
		b = int(self.entry_range_b.get())
		self.game_info.generate_data(a, b)
		self.reset()

	def start(self):
		self.reset()
		self.game_info.op_list.clear()
		if self.game_info.use_builtin.get():
			pass
		else:
			push_swap = subprocess.run(
				[
					self.push_swap_file_name.get(),
					*[str(x) for x in self.game_info.src_data]
				],
				capture_output=True
			)
			self.game_info.op_list = push_swap.stdout.decode('utf-8').rstrip(
			).split('\n')
		self.game_info.op_count = len(self.game_info.op_list)
		self.op_num.config(text=f'operations count = {self.game_info.op_count}')

	def draw(self):
		self.canvas_a.delete('all')
		self.canvas_b.delete('all')
		if len(self.game_info.src_data) == 0:
			return
		delta_x = (self.canvas_a.winfo_width() - 10) / len(self.game_info.src_data)
		delta_y = (self.canvas_a.winfo_height() - 10) / len(self.game_info.src_data)
		for index, x in enumerate(self.game_info.st.stack_a):
			self.canvas_a.create_rectangle(
				0 + 5, index * delta_y + 5,
				x * delta_x + 5, (index + 1) * delta_y + 5,
				width=0,
				fill=self.game_info.colors[x - 1]
			)
		for index, x in enumerate(self.game_info.st.stack_b):
			self.canvas_b.create_rectangle(
				0, (index - 1) * delta_y,
				x * delta_x, index * delta_y,
				width=0,
				fill=self.game_info.colors[x - 1]
			)


def main():
	rand.seed(time.time())
	app = VisuPS(tk.Tk())
	app.root.mainloop()
	return 0


if __name__ == '__main__':
	exit(main())
