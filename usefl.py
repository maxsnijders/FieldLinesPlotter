import fieldlines as fl
import numpy as np
import math

# Copyright Max Snijders 2015
# This code is licenced under a creative commons licence http://creativecommons.org/licenses/by-sa/4.0/
# Any educational use is encouraged 
# Usage: see usefl.py: create a charge configuration, then pass it to fl.plotcharges with the target file name, the charges array and a boolean indicating wether found singularities should be found

def generate_polygon(corners, alternating = False):
	charges = np.array([]);
	current_sign = 1;
	for angle in np.arange(0, 2*math.pi, 2*math.pi/corners):
 		angle += math.pi/4;
		x = 0.5 + np.cos(angle) * 0.3;
		y = 0.5 + np.sin(angle) * 0.3;
		
		if(charges.shape[0] > 0):
			charges = np.vstack((charges,[current_sign,x,y]));
		else:
			charges = np.array([[current_sign,x,y]]);
		if(alternating is True):
			current_sign *= -1;
		
	return charges;
	
def generate_random(count):
	charges = np.array([]);
	for i in np.arange(0, count, 1):
		charge = np.random.rand() * 10 - 5;
		x_pos = np.random.rand();
		y_pos = np.random.rand();
		
		if(charges.shape[0] > 0):
			charges = np.vstack((charges, [charge, x_pos, y_pos]));
		else:
			charges = np.array([[charge, x_pos, y_pos]]);
			
	return charges;
	
#charges = generate_polygon(6,True);	
charges = generate_polygon(4);
#charges = generate_random(4);
#charges = [[1,0.1,0.4],[1,0.4,0.4],[-1,0.7,0.4]];
fl.plotforcharges("freek.png", charges, True);
