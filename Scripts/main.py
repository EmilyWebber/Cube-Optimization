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

	# Need to find the correct starting point 
	params = find_mins(params)

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

		if lowest > 0: 

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

def get_window(w_point, side, params):

	radius = int(params['radius'])

	face = params['sides'][side]

	w1, w2, w3 = w_point[0], w_point[1], w_point[2]

	max_distance = int(radius/2)

	min_distance = max(int(radius/8), 1)

	up = params['w_space_upper_bound']

	outer_cube = int(params['outer_cube_length'])

	if face == 'front' or face == 'back':
		left = max(w1 - max_distance, 0)

		right = min(w1+up-1 + max_distance, outer_cube)

		upwards = min(w3 + max_distance + up-1, outer_cube) 

		down = max(w3-max_distance - (up-1), 0)

	elif face == 'right' or face == 'left':

		left = max(w2 - max_distance, 0)

		right = min(w2+up-1 + max_distance, outer_cube)

		upwards = min(w3 + max_distance + up-1, outer_cube) 

		down = max(w3-max_distance, 0)

	elif face in ['top', 'bottom']:
		left = max(w1 - max_distance, 0)

		right = min(w1+up-1 + max_distance, outer_cube)

		upwards = min(w2 + max_distance + up-1, outer_cube) 

		down = max(w2-max_distance - (up-1), 0)

	return list(range(left, right+1)), list(range(down, upwards+1))

def get_depth(w_point, side, params):
	face = params['sides'][side]
	up = params['w_space_upper_bound']
	w1, w2, w3 = w_point[0], w_point[1], w_point[2]
	outer_cube_length = int(params['outer_cube_length'])
	inside_start = params['inner_cube_lower_left_corner'].split(',')

	x1, y1, z1 = int(inside_start[0]), int(inside_start[1]), int(inside_start[2])

	if face == 'front':
		# check y
		depth = max(w2 - y1,0)

	elif face == 'right':
		# check x
		depth = min(w1-x1, outer_cube_length)

	elif face == 'back':
		# check y
		depth = min(w2 - y1, outer_cube_length)

	elif face == 'left':
		# check x
		depth = max(w1-x1, 0)

	elif face == "top":
		# check z
		depth = min(w3 -z1 , outer_cube_length)

	elif face == "bottom":
		# check z
		depth = max(w3-z1, 0)

	return depth

def get_t_point(row, col, depth, side, param, w_point):
	face = params['sides'][side]

	w1, w2, w3 = int(w_point[0]), int(w_point[1]), int(w_point[2])  

	if face == 'front':
		w2 += depth
		return row, w2, col

	elif face == 'right':
		w1 -= depth
		return w1, row, col

	elif face == 'back':
		w2 -= depth
		return row, w2, col

	elif face == "left":
		w1 += depth
		return w1, row, col

	elif face == 'top':
		w3 -= depth
		return col, row, w3

	elif face == 'bottom':
		w3 += depth
		return col, row, w3

def in_cube(point, params, side):
	face = params['sides'][side]

	x1, y1, z1 = int(point[0]), int(point[1]), int(point[2])

	cube = params['inner_cube_lower_left_corner'].split(',')

	ic_x, ic_y, ic_z = int(cube[0]), int(cube[1]), int(cube[2])

	cube_n = int(params['inner_cube_length'])

	if face == 'front':
		a = ic_x <= x1 <= (ic_x+(cube_n-1))
		b = ic_y == y1 
		c = ic_z <= z1 <= (ic_z + cube_n-1)

	elif face == 'right':
		a = x1 == (ic_x + (cube_n-1))
		b = ic_y <= y1 <= (ic_y + cube_n-1) 
		c = ic_z <= z1 <= (ic_z + cube_n-1)

	elif face == 'back':
		a = ic_x <= x1 <= (ic_x+(cube_n-1))
		b = y1 == ic_y + cube_n-1
		c = ic_z <= z1 <= (ic_z + cube_n-1)

	elif face == 'left':
		a = ic_x == x1
		b = ic_y <= y1 <= (ic_y + cube_n-1) 
		c = ic_z <= z1 <= (ic_z + cube_n-1)

	elif face == 'top':
		a = ic_x <= x1 <= (ic_x + cube_n-1)
		b = ic_y <= y1 <= (ic_y + cube_n-1) 
		c = z1 == ic_z + cube_n-1

	elif face == 'bottom':
		a = ic_x <= x1 <= (ic_x + cube_n-1)
		b = ic_y <= y1 <= (ic_y + cube_n-1) 
		c = z1 == ic_z 

	return a and b and c

def find_matching_tpoints(w_point, side, params):

	t_points = []

	rows, cols = get_window(w_point, side, params)

	# get distance between outer cube and inner cube
	depth = get_depth(w_point, side, params)

	# must have at least a depth of 1 to paint
	if depth == 0:
		return []

	for r in rows:
		for c in cols:
			for d in range(1, depth+1):

				t_p = get_t_point(r,c,d, side, params, w_point)

				if in_cube(t_p, params, side) and not in_cube(w_point, params, side):
					t_points.append(t_p)

	return t_points


def get_pairs(params):

	pairs = {}

	up = params['w_space_upper_bound']

	# loop through the maximum w-space outer bound, and find each corresponding t-space
	for side in range(1, 7):

		for row in range(up):

			for col in range(up):

				# reconstruct the single point to 3D
				w_point = get_3D(row, col, side, params)

				t_spaces = find_matching_tpoints(w_point, side, params)


				if len(t_spaces) >= 1:

					if w_point not in pairs:

						pairs[w_point] = []

					for t in t_spaces:
						pairs[w_point].append(t)



	return pairs



if __name__ == '__main__':
	params = read_params('parameters.txt')

	params = compute_boundary(params)

	print ("Walking through a cubed space of {}".format(params['w_space_upper_bound']))

	pairs = get_pairs(params)

	print (pairs)

	# write_to_disk(pairs)
