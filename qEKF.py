from pyquaternion import Quaternion
import numpy as np
def f(x, u):
	return x*u

def F(x):
	return np.array([[x.w, -x.x, -x.y, -x.z],
									 [x.x, x.w, x.z, -x.y],
									 [x.y, -x.z, x.w, x.x],
									 [x.z, x.y, -x.x, x.w]])
									 
def h(x):
	return x

def H(x):
	return np.array([[x.w, -x.x, -x.y, -x.z],
           [x.x, x.w, x.z, -x.y],
           [x.y, -x.z, x.w, x.x],
           [x.z, x.y, -x.x, x.w]])


def fuse(p, c, init):
	P = np.eye(4)
	V = np.eye(4)
	W = np.eye(4)
	x=init
	fused = []
	fused.append(x)
	for i in range(1, len(p)):
		x = f(x, p[i])
		Fm = F(x)
		P = Fm * P * np.transpose(Fm) + V
		Hm = H(x)
		K = P * np.transpose(H) * np.invert(W + Hm * P * np.transpose(Hm))
		x = Quaternion(np.array(x.elements) * K * (h(x).inverse() * c[i]))
		fused.append(x)
	return fused