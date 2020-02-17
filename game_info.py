import random
import time
from colour import Color
from tkinter import IntVar

import push_swap_stacks

DEFAULT_RANGE_A = 0
DEFAULT_RANGE_B = 100

COLOR_START = "limegreen"
COLOR_END = "orangered"

DEFAULT_SPEED = 500
MINIMUM_SPEED = 1000
SPEED_DELTA = 1.5

STACK_STATE = [
	{'text': '...', 'foreground': 'black'},
	{'text': 'OK', 'foreground': 'green4'},
	{'text': 'KO', 'foreground': 'red2'}
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
		self.op_list = self.st.push_swap()
		self.cur_op = 0
		self.game = 0
		self.speed = DEFAULT_SPEED
		self.op_count = 0
		self.stack_state = 0
		self.use_builtin = IntVar(value=1)

	def reset(self):
		self.cur_op = 0
		self.game = 0
		self.st.new_data(self.src_data)

	def generate_data(self, a, b):
		self.src_data = [x for x in range(a, b)]
		random.shuffle(self.src_data)
		self.colors = list(
			Color(COLOR_START).range_to(Color(COLOR_END), a - b)
		)

	def speed_up(self):
		self.speed = int(self.speed / SPEED_DELTA)

	def speed_down(self):
		self.speed = int(round(self.speed * SPEED_DELTA))
		if self.speed > MINIMUM_SPEED:
			self.speed = MINIMUM_SPEED
		elif self.speed == 0:
			self.speed = 1

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
