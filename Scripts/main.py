import pandas as pd 
import json

def read_params(f_name):
	data = {}
	with open(f_name) as f:
		for row in f.readlines():
			d = row.strip().split()
			if d[0] != 'paint_criteria':
				data[d[0]] = d[-1]
			else:
				data[d[0]] = str(d[-2] + d[-1])
	return data


def get_upper_bound(params):

	outer_cube = int(params['outer_cube_length'])
	inner_cube = int(params['inner_cube_length'])
	radius = int(params['radius'])

	# we'll assume the paint criteria is constant at <= r/2
	rt = inner_cube + int(radius/2)

	assert(rt<=outer_cube)

	return rt


def is_valid(row, col, params):
	return True

def get_space(row, col, side, params, space_type):
	return (row, col, side)

def get_pairs(params):

	pairs = {}

	inner_cube_length = int(params['inner_cube_length'])

	radius = int(params['radius'])

	# pick starting point to paint
	w_space_upper_bound = get_upper_bound(params)

	for side in range(6):

		for row in range(w_space_upper_bound):

			for col in range(w_space_upper_bound):

				if is_valid(row, col, params):

					w_space = get_space(row, col, side, params, 'w')

					t_space = get_space(row, col, side, params, 't')

					if w_space not in pairs:

						pairs[w_space] = []

					pairs[w_space].append(t_space)

if __name__ == '__main__':
	params = read_params('parameters.txt')

	pairs = get_pairs(params)

	# write_to_disk(pairs)