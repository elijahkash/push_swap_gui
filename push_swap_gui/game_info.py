import random
import time
from colour import Color
from tkinter import IntVar
import subprocess

from . import push_swap_stacks
from . import push_swap_algo

DEFAULT_RANGE_A = 0
DEFAULT_RANGE_B = 100

COLOR_START = "limegreen"
COLOR_END = "orangered"

DEFAULT_SPEED = 500
MINIMUM_SPEED = 1000
SPEED_DELTA = 1.5

STATE_TITLE = 'stack_state: '
STACK_STATE = [
	{'text': STATE_TITLE + '...', 'foreground': 'black'},
	{'text': STATE_TITLE + 'OK', 'foreground': 'green4'},
	{'text': STATE_TITLE + 'KO', 'foreground': 'red2'}
]
STATE_NONE = 0
STATE_OK = 1
STATE_KO = 2


class GameInfo:
	def __init__(self):
		self.src_data = []
		self.colors = []
		random.seed(time.time())
		self.generate_data(DEFAULT_RANGE_A, DEFAULT_RANGE_B)
		self.st = push_swap_stacks.PushSwapStacks(self.src_data)
		self.op_list = push_swap_algo.push_swap(self.src_data)
		self.cur_op = 0
		self.game = 0
		self.speed = DEFAULT_SPEED
		self.stack_state = 0
		self.use_builtin = IntVar(value=1)

	def reset(self):
		self.cur_op = 0
		self.game = 0
		self.st.new_data(self.src_data)
		self.update_state()

	def generate_data(self, a, b):
		self.src_data = [x for x in range(a, b)]
		random.shuffle(self.src_data)
		self.colors = list(
			Color(COLOR_START).range_to(Color(COLOR_END), b - a)
		)

	def speed_up(self):
		self.speed = int(self.speed / SPEED_DELTA)

	def speed_down(self):
		self.speed = int(round(self.speed * SPEED_DELTA))
		if self.speed > MINIMUM_SPEED:
			self.speed = MINIMUM_SPEED
		elif self.speed == 0:
			self.speed = 1

	def calc(self, filename):
		self.op_list.clear()
		if self.use_builtin.get():
			self.op_list = push_swap_algo.push_swap(self.src_data)
		else:
			push_swap = subprocess.run(
				[filename, *[str(x) for x in self.src_data]],
				capture_output=True
			)
			self.op_list = push_swap.stdout.decode('utf-8').rstrip().split('\n')
		self.update_state()

	def start_game(self):
		if self.game or self.cur_op == len(self.op_list):
			self.game = 0
		else:
			self.game = time.time()

	def next_op(self):
		self.st.cmd[self.op_list[self.cur_op]]()
		self.cur_op += 1
		if (self.cur_op == len(self.op_list)):
			self.update_state()
			self.game = 0

	def update_state(self):
		if self.cur_op != len(self.op_list):
			self.stack_state = STATE_NONE
		elif (
			len(self.src_data) == len(self.st.stack_a) and all(
				self.st.stack_a[i] < self.st.stack_a[i + 1]
				for i in range(len(self.src_data) - 1))
		):
			self.stack_state = STATE_OK
		else:
			self.stack_state = STATE_KO
