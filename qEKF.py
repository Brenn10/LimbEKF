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
	return np.eye(4)


def fuse(p, c, init):
	P = np.eye(4)
	V = np.eye(4)*1e-1
	W = np.eye(4)*1e2
	x=init
	fused = []
	fused.append(x)
	for i in range(1, len(p)):
		x = f(x, p[i])
		Fm = F(x)
		P = Fm @ P @ np.transpose(Fm) + V
		Hm = H(x)
		K = P @ np.transpose(Hm) @ np.linalg.inv(W + Hm @ P @ np.transpose(Hm))

		xpre = np.reshape(np.array(x.elements), (4, 1))
		corr = np.reshape(np.array((c[i].elements - h(x).elements)), (4, 1))
		newq = xpre + K @ corr
		x = Quaternion(list(newq))
		fused.append(x)
	return fused
