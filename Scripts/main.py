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

	x_0, y_0, z_0 = params['x_min'], params['y_min'], params['z_min']

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

		# z is constant
		z = z_0 + up - 1

	elif face == 'bottom':

		x = x_0 + row

		y = y_0 + col

		# z is constant
		z = z_0 - (up- 1)

	return x, y, z

def compute_boundary(params):

	params['sides'] = {1:"front",  2:'right', 3:'back', 4:'left', 5:'top', 6:'bottom' }

	up = get_upper_bound(params)

	params['w_space_upper_bound'] = up

	start = params['inner_cube_lower_left_corner'].split(',')

	x_0, y_0, z_0 = int(start[0]), int(start[1]), int(start[2])

	params['start'] = [x_0, y_0, z_0]

	return params

def find_mins(params):
	'''
	This function finds the minimal starting point for the cube
		On the lower left side
	'''
	outer = int(params['outer_cube_length'])

	radius = int(params['radius'])
	variables = [params['start'][0], params['start'][1], params['start'][2]]
	strs = ['x', 'y', 'z']
	# assume the lower bound on distance is radius / 8
	
	# if there is not enough space, set range to outer cube length
	
	for idx, v in enumerate(variables):
		var_str = strs[idx]
		low_key = '{}_min'.format(var_str)

		# Get the absolute minimum required space

		lowest = v - int(radius/8)

		if lowest >= 0: 

			# get the most space you can
			max_var = v - int(radius/2)

			if max_var > 0:
				params[low_key] = max_var

			else:
				params[low_key] = 0

		else:

			# get what's available
			params[low_key] = 0

	return params

def find_matching_tpoints(w_point, side, params):
	w1, w2, w3 = w_point[0], w_point[1], w_point[2]

	t_points = []
	radius = int(params['radius'])
	face = params['sides'][side]

	print ('w point ', w_point, face)

	max_distance = int(radius/2)
	min_distance = int(radius/8)

	print ('have a max distance of ', max_distance)

	if face == 'front':
		# look left
		window = w1 - max_distance

		if w1 <= params['x_min'] and w1 >= 0:


		# look right
		window = w1 + max_distance

		# look up
		window = 

		# look down
		window = 

	elif face == 'right':
		# look left
		window = w1 - max_distance
		# if w1 <= params['x_min'] and w1 >= 0:

		# look right
		window = w1 + 2

		# look up
		window = 

		# look down
		window = 

	elif face == 'back':
			# look left
		window = w1 - 2
		# if w1 <= params['x_min'] and w1 >= 0:

		# look right
		window = w1 + 2

		# look up
		window = 

		# look down
		window = 


	elif face = 'left':
			# look left
		window = w1 - 2
		# if w1 <= params['x_min'] and w1 >= 0:

		# look right
		window = w1 + 2

		# look up
		window = 

		# look down
		window = 


	elif face == 'top':
		# look left
		window = w1 - 2
		# if w1 <= params['x_min'] and w1 >= 0:

		# look right
		window = w1 + 2

		# look up
		window = 

		# look down
		window = 

	elif face == 'botom':
		# look left
		window = w1 - 2
		# if w1 <= params['x_min'] and w1 >= 0:

		# look right
		window = w1 + 2

		# look up
		window = 

		# look down
		window = 

	return []


def get_pairs(params):

	pairs = {}

	up = params['w_space_upper_bound']

	# Need to find the correct starting point 
	ranges = find_mins(params)

	# loop through the maximum w-space outer bound, and find each corresponding t-space
	for side in range(1, 7):

		for row in range(up):

			for col in range(up):

	# 			# reconstruct the single point to 3D
				w_point = get_3D(row, col, side, params)

				t_spaces = find_matching_tpoints(w_point, side, params)

				return

				# if len(t_spaces) >= 1:

				# 	if w_space not in pairs:

				# 		pairs[w_space] = []

				# 	for t in t_spaces:
				# 		pairs[w_space].append(t

	return pairs



if __name__ == '__main__':
	params = read_params('parameters.txt')

	params = compute_boundary(params)

	print ("Walking through a cubed space of {}".format(params['w_space_upper_bound']))

	pairs = get_pairs(params)

	# write_to_disk(pairs)


# TO-DO
# 1. Implement an in_cube() function
# 2. Find the spots to search 

