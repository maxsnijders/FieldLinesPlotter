import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.colors as col;
import fieldline as fl

# Copyright Max Snijders 2015
# This code is licenced under a creative commons licence http://creativecommons.org/licenses/by-sa/4.0/
# Any educational use is encouraged 
# Usage: see usefl.py: create a charge configuration, then pass it to fl.plotcharges with the target file name, the charges array and a boolean indicating wether found singularities should be found


FL_PER_CHARGE = 32;
FL_DIST_FROM_CHARGE = 0.01;
FL_STEP_SIZE = 0.001;
FL_STEP_LIM = 3000;
FL_SOURCE_MIN_DIST = FL_STEP_SIZE;
FL_SING_LIM = 0.5;

def nparr_vstack(arr, addition):
	if(arr.size > 0):
		return np.vstack((arr, addition));
	else:
		return np.array([addition]);
		
def step_dir(pos_x, pos_y, charges):
	field_x = 0;
	field_y = 0;
	
	for charge in charges:
		charge_x = charge[1];
		charge_y = charge[2];
		charge_charge = charge[0];
		
		dist_x = charge_x - pos_x;
		dist_y = charge_y - pos_y;
		
		angle = np.arctan2(dist_y, dist_x);
		
		dist = math.sqrt(dist_x**2 + dist_y**2);
		if(dist < FL_SOURCE_MIN_DIST):
			return (False, 'charge');
		
		emf_c_x = -1 * charge_charge / dist**2 * np.cos(angle);
		emf_c_y = -1 * charge_charge / dist**2 * np.sin(angle);
		
		field_x += emf_c_x;
		field_y += emf_c_y;
	
	total_field = math.sqrt(field_x**2 + field_y**2);
	if(total_field < FL_SING_LIM):
		return (False, 'singularity');
			
	return (True, np.arctan2(field_y, field_x));

def field_at_point(pos_x, pos_y, charges):
	field_x = 0;
	field_y = 0;
	
	for charge in charges:
		charge_x = charge[1];
		charge_y = charge[2];
		charge_charge = charge[0];
		
		dist_x = charge_x - pos_x;
		dist_y = charge_y - pos_y;
		
		angle = np.arctan2(dist_y, dist_x);
		
		dist = math.sqrt(dist_x**2 + dist_y**2);
		if(dist < FL_SOURCE_MIN_DIST):
			return 1;
		
		emf_c_x = -1 * charge_charge / dist**2 * np.cos(angle);
		emf_c_y = -1 * charge_charge / dist**2 * np.sin(angle);
		
		field_x += emf_c_x;
		field_y += emf_c_y;
	
	total_field = math.sqrt(field_x**2 + field_y**2);
	return total_field;
			
def search_minimum(step_size, searchpoints = False, charges = np.array([])):
	if(searchpoints is False): #Generate them
		searchpoints = np.array([]);
		for x in np.arange(0, 1, step_size):
			for y in np.arange(0, 1, step_size):
				searchpoints = nparr_vstack(searchpoints, np.array([x, y]));
	
	newsearchpoints = np.array([]);
	for point in searchpoints:	
		x = point[0];
		y = point[1];
		minimum = True;
		field = field_at_point(x, y, charges);
		for a in np.arange(0, 2*math.pi, 2*math.pi/8):
			neighbour_field = field_at_point(x + np.cos(a) * 0.05, y + 
                                             np.sin(a) * 0.05, charges);
			if(field > neighbour_field):
				minimum = False;			
		if(minimum):
			newsearchpoints = nparr_vstack(newsearchpoints, np.array([x, y]));		
	
	return newsearchpoints;
	
def plotforcharges(name, charges, searchforsingularities = False):
	#generate the fl sources
	fl_sources = np.array([]);
	for charge in charges:
		charge_x = charge[1];
		charge_y = charge[2];
		for angle in np.arange(0, 2*math.pi, 2*math.pi/FL_PER_CHARGE):
			source_x = charge_x + FL_DIST_FROM_CHARGE * np.cos(angle);
			source_y = charge_y + FL_DIST_FROM_CHARGE * np.sin(angle);
			fl_sources = nparr_vstack(fl_sources, [charge[0], 
													source_x, source_y]);
			
	fls = np.array([]);
	#We calculate the field line properties
	for fl_source in fl_sources:
		fl_obj = fl.Fieldline();
		cur_x = fl_source[1];
		cur_y = fl_source[2];
		fl_obj.steps = np.array([[cur_x, cur_y]]);
		fl_obj.fl_source_charge = fl_source[0];
		running = True;
		while(running):
			#We make a step
			dir = step_dir(cur_x, cur_y, charges);
			if(dir[0] is False):
				if(dir[1] is 'charge'):	
					fl_obj.fl_term_in_charge = True;
				elif(dir[1] is 'singularity'):
					fl_obj.fl_term_in_sing   = True;
				running = False;
				break;
			
			dir = dir[1];
				
			if(fl_source[0] < 0):
				dir += math.pi;
				
			step_x = np.cos(dir) * FL_STEP_SIZE;
			step_y = np.sin(dir) * FL_STEP_SIZE;
			
			#We record this step.
			cur_x += step_x;
			cur_y += step_y;
			fl_obj.steps = np.vstack((fl_obj.steps, [cur_x, cur_y]));
			fl_obj.fl_step_count += 1;
		
			#We check for termination
			if(fl_obj.fl_step_count > FL_STEP_LIM):
				running = False;
		
		if((fl_obj.fl_term_in_charge is False) and 
			(fl_obj.fl_term_in_sing is False)):
			fl_obj.fl_arrow_pos = 0.3 / FL_STEP_SIZE;
		else:
			fl_obj.fl_arrow_pos = fl_obj.fl_step_count / 2;
			
		cur_x = fl_source[1];
		cur_y = fl_source[2];
		prev_x = 0;
		prev_y = 0;
		cur_angle = 0;
		for step in np.arange(0, fl_obj.fl_arrow_pos, 1):
			prev_x = cur_x;
			prev_y = cur_y;
			
			#We make a step
			dir = step_dir(cur_x, cur_y, charges);
			if(dir[0] is False):
				running = False;
				break;
			
			dir = dir[1];
				
			if(fl_source[0] < 0):
				dir += math.pi;
				
			step_x = np.cos(dir) * FL_STEP_SIZE;
			step_y = np.sin(dir) * FL_STEP_SIZE;	
			cur_x += step_x;
			cur_y += step_y;
			
			#Calculate angle.
			dx = cur_x - prev_x;
			dy = cur_y - prev_y;
			cur_angle = np.arctan2(dy,dx);
			
		fl_obj.arrow_x = cur_x;
		fl_obj.arrow_y = cur_y;
		if(fl_source[0] < 0):
			cur_angle += math.pi;
			
		fl_obj.arrow_angle = cur_angle;
		
		fls = nparr_vstack(fls, fl_obj);
		
		
	#We now plot all paths
	fig = plt.figure();
	ax = fig.add_subplot(111)
	for fl_obj in fls:
		charge  = fl_obj[0].fl_source_charge
		tocharge= fl_obj[0].fl_term_in_charge;
		
		if(not(charge < 0 and tocharge is True)):
			ax.plot(fl_obj[0].steps[:,0],fl_obj[0].steps[:,1], c='black', zorder=1);
	
	#We draw the arrows;
	for fl_obj in fls:
		arrow_x = fl_obj[0].arrow_x;
		arrow_y = fl_obj[0].arrow_y;
		angle   = fl_obj[0].arrow_angle;
		charge  = fl_obj[0].fl_source_charge
		tocharge= fl_obj[0].fl_term_in_charge;
		
		if(not(charge < 0 and tocharge is True)):
			ax.scatter(arrow_x, arrow_y, s=100, 
						marker=(3, 0, np.degrees(angle) + 30), 
						zorder=2, c='black');

	#Plot the point charges
	for charge in charges:
		ax.scatter(charge[1], charge[2], s=100 * abs(charge[0]), 
					marker='o', c='blue', zorder=3);
		size = abs(charge[0]) * 60;
		if(charge[0] > 0):
			ax.scatter(charge[1]-0.001, charge[2]-0.001,
					 s=size, marker='$+$', zorder=4);
		elif(charge[0] < 0):
			ax.scatter(charge[1]-0.002, charge[2]-0.005,
					 s=size, marker='$-$', zorder=4);
	
	#We now search for singularities
	
	if(searchforsingularities is True):
		for x in np.arange(0, 1, FL_STEP_SIZE):
			for y in np.arange(0, 1, FL_STEP_SIZE):
				field_strength = field_at_point(x, y, charges);
				if(field_strength < FL_SING_LIM):
					ax.scatter(x, y, s=60, marker='o', c='red', zorder=5);	
					
	ax.set_xlabel("X Pos");
	ax.set_aspect('equal');
	ax.set_ylabel("Y Pos");
	ax.set_xlim(0,1);
	ax.set_ylim(0,1);
	ax.set_title("Field Lines");
	fig.savefig(name);
