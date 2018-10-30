import numpy as np

# Copyright Max Snijders 2015
# This code is licenced under a creative commons licence http://creativecommons.org/licenses/by-sa/4.0/
# Any educational use is encouraged 
# Usage: see usefl.py: create a charge configuration, then pass it to fl.plotcharges with the target file name, the charges array and a boolean indicating wether found singularities should be found

class Fieldline:
	fl_step_count = 0;
	fl_steps = np.array([]);
	fl_arrow_pos = 0;
	fl_arrow_x = 0;
	fl_arrow_y = 0;
	fl_term_in_charge = False;
	fl_term_in_sing   = False;
	fl_arrow_angle = 0;
	fl_source_charge = 1;