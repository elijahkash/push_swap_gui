import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import ttk

import game_info

# TODO: depend from display?
# w = root.winfo_screenwidth()
# h = root.winfo_screenheight()

DEFAULT_WIN_SIZE_X = 1000
DEFAULT_WIN_SIZE_Y = 1000
MIN_SIZE_X = 700
MIX_SIZE_Y = 650

WIN_TITLE = 'push-swap_python'
APP_THEME = 'aqua'


class PushSwapGUI:
	def __init__(self, master):
		self.master = master
		self.master.geometry(f'{DEFAULT_WIN_SIZE_X}x{DEFAULT_WIN_SIZE_Y}+0+0')
		self.master.minsize(MIN_SIZE_X, MIX_SIZE_Y)
		self.master.title(WIN_TITLE)
		self.style = ttk.Style(self.master)
		self.style.theme_use(APP_THEME)
		self.game_info = game_info.GameInfo()
		self.init_gui()
		self.update_labels()
		self.grid_gui()
		self.master.update()
		self.draw()

	def init_gui(self):
		self.frame_root = ttk.Frame(self.master, padding='5 2 5 2')
		self.canvas_a = tk.Canvas(self.frame_root)
		self.canvas_b = tk.Canvas(self.frame_root)
		self.cmd_list = scrolledtext.ScrolledText(
			self.frame_root, width=5, state='disable'
		)
		self.frame_menu = ttk.Frame(self.frame_root)
		self.button_quit = ttk.Button(
			self.frame_menu, text='Quit', command=self.quit_from_app
		)
		self.button_calc = ttk.Button(
			self.frame_menu, text='Calculate', command=self.calc
		)
		self.button_speed_down = ttk.Button(
			self.frame_menu, text='<<', command=self.speed_down
		)
		self.button_game = ttk.Button(
			self.frame_menu, text='▷', command=self.game
		)
		self.button_speed_up = ttk.Button(
			self.frame_menu, text='>>', command=self.speed_up
		)
		self.button_reset = ttk.Button(
			self.frame_menu, text='Reset', command=self.reset
		)
		self.button_generate_new_data = ttk.Button(
			self.frame_menu, text='Generate new [a, b)',
			command=self.generate_new_data
		)
		self.entry_range_a = ttk.Entry(self.frame_menu, width=10)
		self.entry_range_a.insert(0, str(game_info.DEFAULT_RANGE_A))
		self.entry_range_b = ttk.Entry(self.frame_menu, width=10)
		self.entry_range_b.insert(0, str(game_info.DEFAULT_RANGE_B))
		self.label_range_a = ttk.Label(self.frame_menu, text='<- input a')
		self.label_range_b = ttk.Label(self.frame_menu, text='<- input b')
		self.switch_builtin = ttk.Checkbutton(
			self.frame_menu, text='use built-in algo',
			command=self.builtin, variable=self.game_info.use_builtin
		)
		self.label_file_name = ttk.Label(
			self.frame_menu, text='Custom push_swap:'
		)
		self.entry_file_name = ttk.Entry(
			self.frame_menu, width=30, state=tk.DISABLED
		)
		self.button_open_file = ttk.Button(
			self.frame_menu, text='choose file ...', command=self.choose_file,
			state=tk.DISABLED
		)
		self.label_speed = ttk.Label(self.frame_menu)
		self.label_op_num = ttk.Label(self.frame_menu)
		self.label_curr_op = ttk.Label(self.frame_menu)
		self.label_stack_state = ttk.Label(self.frame_menu)
		self.label_poweredby = ttk.Label(
			self.frame_menu, text='powered by Ilya Kashnitkiy', anchor=tk.CENTER
		)
		self.label_git_link = ttk.Label(
			self.frame_menu, text='github.com/elijahkash', anchor=tk.CENTER
		)

	def grid_gui(self):
		STICKY_FULL = {'sticky': (tk.W, tk.E, tk.N, tk.S)}
		self.master.columnconfigure(0, weight=1)
		self.master.rowconfigure(0, weight=1)
		self.frame_root.grid(**STICKY_FULL)
		self.frame_root.rowconfigure(0, weight=1)
		self.frame_root.columnconfigure(0, weight=1)
		self.frame_root.columnconfigure(1, weight=20)
		self.frame_root.columnconfigure(2, weight=20)
		self.frame_root.columnconfigure(3, weight=1)
		self.canvas_a.grid(column=1, row=0, pady=4, padx=2, **STICKY_FULL)
		self.canvas_b.grid(column=2, row=0, pady=4, padx=2, **STICKY_FULL)
		self.cmd_list.grid(column=3, row=0, pady=4, **STICKY_FULL)
		self.frame_menu.grid(column=0, row=0, pady=4, padx=4, **STICKY_FULL)
		for i in range(0, 3):
			self.frame_menu.columnconfigure(i, weight=1)
		for i in range(0, 90):
			self.frame_menu.rowconfigure(i, weight=1)
		self.button_quit.grid(row=0, columnspan=3, **STICKY_FULL)
		self.button_calc.grid(row=1, columnspan=3, **STICKY_FULL)
		self.button_speed_down.grid(row=2, column=0, **STICKY_FULL)
		self.button_game.grid(row=2, column=1, **STICKY_FULL)
		self.button_speed_up.grid(row=2, column=2, **STICKY_FULL)
		self.button_reset.grid(row=3, columnspan=3, **STICKY_FULL)
		self.button_generate_new_data.grid(row=4, columnspan=3, **STICKY_FULL)
		self.entry_range_a.grid(row=5, column=0)
		self.entry_range_b.grid(row=6, column=0)
		self.label_range_a.grid(row=5, column=2, **STICKY_FULL)
		self.label_range_b.grid(row=6, column=2, **STICKY_FULL)
		self.switch_builtin.grid(row=7, column=0, **STICKY_FULL)
		self.label_file_name.grid(row=8, column=1, **STICKY_FULL)
		self.entry_file_name.grid(
			in_=self.frame_menu, row=9, columnspan=3, **STICKY_FULL
		)
		self.button_open_file.grid(row=8, column=2, **STICKY_FULL)
		self.label_speed.grid(row=13, column=0, columnspan=3, **STICKY_FULL)
		self.label_op_num.grid(row=14, column=0, columnspan=3, **STICKY_FULL)
		self.label_curr_op.grid(row=15, column=0, columnspan=3, **STICKY_FULL)
		self.label_stack_state.grid(
			row=16, column=0, columnspan=3, **STICKY_FULL
		)
		self.label_poweredby.grid(row=40, column=0, columnspan=3, **STICKY_FULL)
		self.label_git_link.grid(row=41, column=0, columnspan=3, **STICKY_FULL)

	def update_labels(self):
		self.button_game.config(text='||' if self.game_info.game else '▷')
		self.label_speed.config(
			text=f'speed (delay between ops in msec): {self.game_info.speed}'
		)
		self.label_op_num.config(
			text=f'operations count = {len(self.game_info.op_list)}'
		)
		self.label_curr_op.config(
			text=f'current operation: {self.game_info.cur_op}'
		)
		self.label_stack_state.config(
			game_info.STACK_STATE[self.game_info.stack_state]
		)

	def quit_from_app(self):
		self.master.destroy()

	def calc(self):
		self.reset()
		self.game_info.calc(self.entry_file_name.get())
		self.update_labels()

	def speed_down(self):
		self.game_info.speed_down()
		self.update_labels()

	def speed_up(self):
		self.game_info.speed_up()
		self.update_labels()

	def game(self):
		self.game_info.start_game()
		self.next_op(self.game_info.game)

	def reset(self):
		self.game_info.reset()
		self.draw()
		self.update_labels()
		self.cmd_list_clean()

	def generate_new_data(self):
		a = int(self.entry_range_a.get())
		b = int(self.entry_range_b.get())
		self.game_info.generate_data(a, b)
		self.reset()

	def builtin(self):
		if self.game_info.use_builtin.get():
			value = tk.DISABLED
		else:
			value = tk.NORMAL
		self.button_open_file.config(state=value)
		self.entry_file_name.config(state=value)

	def choose_file(self):
		tmp = filedialog.askopenfilename()
		if tmp:
			self.entry_file_name.delete(0, tk.END)
			self.entry_file_name.insert(0, tmp)

	def draw(self):
		self.canvas_a.delete('all')
		self.canvas_b.delete('all')
		if len(self.game_info.src_data) == 0:
			return
		delta_x = (self.canvas_a.winfo_width() - 10) \
			/ len(self.game_info.src_data)
		delta_y = (self.canvas_a.winfo_height() - 10) \
			/ len(self.game_info.src_data)
		for index, x in enumerate(self.game_info.st.stack_a):
			self.draw_item(self.canvas_a, index, x, delta_x, delta_y)
		for index, x in enumerate(self.game_info.st.stack_b):
			self.draw_item(self.canvas_b, index, x, delta_x, delta_y)

	def draw_item(self, canvas, index, x, delta_x, delta_y):
		canvas.create_rectangle(
			0 + 5, index * delta_y + 5,
			x * delta_x + 5, (index + 1) * delta_y + 5,
			width=0,
			fill=self.game_info.colors[x - 1]
		)

	def next_op(self, game):
		if self.game_info.cur_op == len(self.game_info.op_list):
			self.update_labels()
			self.draw()
			return
		if game != self.game_info.game:
			return
		self.game_info.next_op()
		if self.game_info.speed or self.game_info.cur_op % 128 == 0:
			self.update_labels()
			self.draw()
			self.master.update()
		self.cmd_list_insert(self.game_info.op_list[self.game_info.cur_op - 1])
		self.master.after(self.game_info.speed, self.next_op, game)

	def cmd_list_clean(self):
		self.cmd_list.config(state='normal')
		self.cmd_list.delete(1.0, tk.END)
		self.cmd_list.config(state='disabled')

	def cmd_list_insert(self, next_cmd):
		self.cmd_list.config(state='normal')
		self.cmd_list.insert(tk.END, next_cmd + '\n')
		self.cmd_list.yview(tk.END)
		self.cmd_list.config(state='disabled')


def main():
	master = tk.Tk()
	PushSwapGUI(master)
	master.mainloop()
	return 0


if __name__ == '__main__':
	exit(main())
