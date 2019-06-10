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

def get_3D(row, col, side, params):
	'''
	This function reconstructs a given point into 3D space
		Adds positioning by the lower left corner of the cube
		Changes per face
	Position is always: (x,y,z)
	'''
	up = params['w_space_upper_bound']

	x_0, y_0, z_0 = params['start'][0], params['start'][1], params['start'][2]

	face = params['sides'][side]

	if face == 'front':

		x = x_0 + row 

		# Y is constant
		y = y_0 

		z = z_0 + col

	elif face == 'right':

		# X is constant, subtract 1 for computer indexing
		x = x_0 + up-1

		y = y_0 + col

		z = z_0 + row

	elif face == 'back':

		x = x_0 + row 

		# Y is constant
		y = y_0 + up - 1

		z = z_0 + col

	elif face == 'left':

		# x is constant
		x = x_0 

		y = y_0 + col 

		z = z_0 + row

	elif face == 'top':

		x = x_0 + row

		y = y_0 + col

		z = z_0 + up - 1

	elif face == 'bottom':

		x = x_0 + row

		y = y_0 + col

		z = z_0 - (up- 1)

	if face == 'bottom':
		print (x, y, z, face)

	return x_0, y_0, z_0

def find_matching_tpoints(row, col, side, params):

	t_space = []

	w_space = get_space(row, col, side, params, 'w')

	return row, [col], True

def compute_boundary(params):

	params['sides'] = {1:"front",  2:'right', 3:'back', 4:'left', 5:'top', 6:'bottom' }

	up = get_upper_bound(params)

	params['w_space_upper_bound'] = up

	start = params['inner_cube_lower_left_corner'].split(',')

	x_0, y_0, z_0 = int(start[0]), int(start[1]), int(start[2])

	params['start'] = [x_0, y_0, z_0]

	return params


def get_pairs(params):

	pairs = {}

	up = params['w_space_upper_bound']

	# loop through the maximum w-space outer bound, and find each corresponding t-space
	for side in range(1, 7):

		for row in range(up):

			for col in range(up):

				# reconstruct the single point to 3D
				w_point = get_3D(row, col, side, params)

				# w_space, t_spaces, valid = find_matching_tpoints(row, col, side, params)

				# if valid:

				# 	if w_space not in pairs:

				# 		pairs[w_space] = []

				# 	for t in t_spaces:
				# 		pairs[w_space].append(t

	return pairs



if __name__ == '__main__':
	params = read_params('parameters.txt')

	params = compute_boundary(params)

	print ("Walking through a cubed space of {}".format(params['w_space_upper_bound']))

	pirs = get_pairs(params)

	# write_to_disk(pairs)


