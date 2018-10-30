import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.colors as col;

epsilon_0 = 8.9*10**(-12);

point_charges = np.array([[0.25,0.25],[0.75,0.25],[0.75,0.75],[0.25,0.75]]);
ef_vectors = np.array([]);

step = 0.05

X = np.arange(0,1,step);
Y = np.arange(0,1,step);
Steps = 1/step;
U = np.zeros((Steps, Steps));
V = np.zeros((Steps, Steps));

xindex = 0;
for x in X:
	yindex = 0;
	for y in Y:
		#We now calculate the nett EF
		ef_x = 0;
		ef_y = 0;
		total_ef = 0;
		for charge in point_charges:
			x_pos = charge[0];
			y_pos = charge[1];
			
			x_dis = x_pos - x;
			y_dis = y_pos - y;
			
			total_dis = math.sqrt(x_dis**2 + y_dis**2);
			
			if(total_dis > 0.01):
				total_ef = -1/(4 * math.pi * epsilon_0) * 
							0.01/(total_dis**2);
			else:
				total_ef = 0;
				
			angle = np.arctan2(x_dis,y_dis);
			ef_x += total_ef * np.cos(angle);
			ef_y += total_ef * np.sin(angle);
				
		U[xindex][yindex] = ef_x;
		V[xindex][yindex] = ef_y;	
		
		yindex += 1;
	xindex += 1;



plt.figure()
ax = plt.gca()
ax.quiver(X,Y,U,V);
ax.set_xlim([0,1])
ax.set_ylim([0,1])
ax.set_title("EM Vectoren in het veld");
ax.set_xlabel("X Pos");
ax.set_aspect('equal');
ax.set_ylabel("Y Pos");
plt.draw()
plt.savefig("vectors.png");