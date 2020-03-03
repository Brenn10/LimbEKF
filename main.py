from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from matplotlib import pyplot as plt
import numpy as np
import loadData
import pickle
import qEKF
from pyquaternion import Quaternion
m = pickle.load(open("save.p", "rb"))
fused = qEKF.fuse(m.s.p, m.s.ori, Quaternion(.5,.5,.5,-.5))

q_fix_1 = Quaternion([0.155,-0.735,-0.190,0.632])

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
colors = ['r', 'g', 'b', 'r', 'g', 'b']
lines = sum([ax.plot([], [], [], c=c)
             for c in colors], [])

startpoints = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [
                       0, 0, 0], [0, 0, 0], [0, 0, 0]])
endpoints = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1],
                      [1, 0, 0], [0, 1, 0], [0, 0, 1]])

ax.set_xlim((-3,3))
ax.set_ylim((-3,3))
ax.set_zlim((-3,3))

ax.view_init(30, 0)

for line in lines:
        line.set_data([], [])
        line.set_3d_properties([])

def init():
    for line in lines:
        line.set_data([], [])
        line.set_3d_properties([])

    return lines

def animate(i):
	q1 = fused[i] #*q_fix_1
	q2 = m.s.ori[i]
	qN=0
	for line, start, end in zip(lines, startpoints, endpoints):
		if(qN<3):
			start = q1.rotate(start)
			end = q1.rotate(end)
		else:

			start = q2.rotate(start)
			end = q2.rotate(end)

		line.set_data([start[0], end[0]], [start[1], end[1]])
		line.set_3d_properties([start[2], end[2]])
		qN += 1
	fig.canvas.draw()
	return lines

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=7400, interval=50, blit=False)

plt.show()
