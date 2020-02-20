from . import push_swap_stacks


def push_swap(src_data):
	st = push_swap_stacks.PushSwapStacks(src_data)
	res = [] if len(src_data) != 3 else sort_three(st)
	sorted_seq = max_sorted_seq(st)
	while len(st.stack_a) > len(sorted_seq):
		if st.stack_a[0] not in sorted_seq:
			res.append(st.do_cmd('pb'))
		else:
			res.append(st.do_cmd('ra'))
	while st.stack_b:
		res.extend(insert_next(st, *find_best(st)))
	res.extend(align_stack(st))
	return res


def sort_three(st):
	res = []
	max_val = max(st.stack_a)
	min_val = min(st.stack_a)
	if (st.stack_a[0] == max_val and st.stack_a[1] != min_val) or \
		(st.stack_a[2] == max_val and st.stack_a[0] != min_val) or \
		(st.stack_a[1] == max_val and st.stack_a[2] != min_val):
		res.append(st.do_cmd('sa'))
	return res


def align_stack(st):
	pos = st.stack_a.index(1)
	if pos > len(st.stack_a) - pos:
		return(['rra'] * (len(st.stack_a) - pos))
	else:
		return(['ra'] * pos)


def max_sorted_seq(st):
	aligned_st = st.stack_a.copy()
	aligned_st.rotate(-aligned_st.index(1))
	dyn_vals = [0] * len(aligned_st)
	for i, x in enumerate(aligned_st):
		tmp = []
		for j, y in enumerate(reversed(dyn_vals[:i])):
			if aligned_st[i - 1 - j] < x:
				tmp.append(y + 1)
		dyn_vals[i] = max(tmp, default=0)
	aligned_st.reverse()
	dyn_vals.reverse()
	cur_val = max(dyn_vals)
	res = []
	for i, x in enumerate(dyn_vals):
		if x == cur_val and (len(res) == 0 or aligned_st[i] < res[0]):
			res.insert(0, aligned_st[i])
			cur_val -= 1
	return res


def find_best(st):
	res = (-len(st.stack_a), len(st.stack_b))
	for i, x in enumerate(st.stack_b):
		if count_ops(i, 0) >= count_ops(*res):
			break
		tmp = (find_place(st, x), i)
		if count_ops(*tmp) < count_ops(*res):
			res = tmp
		tmp = (find_place(st, st.stack_b[-i]), -i)
		if count_ops(*tmp) < count_ops(*res):
			res = tmp
	return res


def find_place(st, x):
	for i in range(len(st.stack_a)):
		if x < st.stack_a[i] and x > st.stack_a[i - 1]:
			return i
		if x > st.stack_a[-i] and x < st.stack_a[-i + 1]:
			return -i + 1
	max_val_pos = st.stack_a.index(max(st.stack_a)) + 1
	if max_val_pos == len(st.stack_a):
		max_val_pos = 0
	if max_val_pos > len(st.stack_a) - max_val_pos:
		max_val_pos = -(len(st.stack_a) - max_val_pos)
	return max_val_pos


def count_ops(pos_a, pos_b):
	if pos_a * pos_b > 0:
		return max(abs(pos_a), abs(pos_b))
	else:
		return abs(pos_a) + abs(pos_b)


def insert_next(st, pos_a, pos_b):
	res = []
	if (pos_a * pos_b > 0):
		tmp = min(pos_a, pos_b) if pos_a > 0 else max(pos_a, pos_b)
		op = 'rr' if pos_a > 0 else 'rrr'
		st.stack_a.rotate(-tmp)
		st.stack_b.rotate(-tmp)
		res.extend([op] * abs(tmp))
		pos_a -= tmp
		pos_b -= tmp
	op = 'ra' if pos_a > 0 else 'rra'
	st.stack_a.rotate(-pos_a)
	res.extend([op] * abs(pos_a))
	op = 'rb' if pos_b > 0 else 'rrb'
	res.extend([op] * abs(pos_b))
	st.stack_b.rotate(-pos_b)
	res.append(st.do_cmd('pa'))
	return res
