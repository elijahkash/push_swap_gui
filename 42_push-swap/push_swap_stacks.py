from collections import deque


class PushSwapStacks:
	"""
	describe stacks for push-swap algorithm
	"""

	def __init__(self, initstate):
		""" initstate: Iterable[_T]=..."""
		self.stack_a = deque()
		self.stack_b = deque()
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

	def do_cmd(self, op):
		self.cmd[op]()
		return op

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
