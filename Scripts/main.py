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


def get_starting_point(params):
	return (params['inner_cube_lower_left_corner'])

def is_valid(row, col, params):
	return True

def get_space(row, col, side, params, space_type):
	return (0,0,0)





def get_pairs(params):

	pairs = {}

	inner_cube_length = int(params['inner_cube_length'])

	radius = int(params['radius'])

	# pick starting point to paint
	starting_point = get_starting_point(params)

	for side in range(6):
		print ("walking down side ", side)

		for row in range(inner_cube_length):

			for col in range(inner_cube_length):

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