from oct2py import octave
import numpy as np
from pyquaternion import Quaternion
from LoadedData import LoadedData

def fixNan(A):
	i=0
	while(i<len(A)):
		si = i - 1
		ei = i+1 
		if (np.isnan(np.sum(A[i]))):
			while (np.isnan(np.sum(A[ei]))):
				ei += 1
			slope = (A[ei] - A[si]) / (ei - si)
			for i in range(1, ei - si + 1):
				A[si+i]= A[si]+slope*i
		i = ei
	return A

def quatFromAxes(x, y, z,debug=False):
	q=[]
	for i in range(np.size(x,axis=0)):
		R = np.array([x[i]/np.linalg.norm(x[i]), y[i] /
                    np.linalg.norm(y[i]), z[i] / np.linalg.norm(z[i])])
		q.append(Quaternion(matrix=R))
	return q

def quatFromAccMag(acc,mag):
	q = []
	for i in range(np.size(acc, axis=0)):
		z = acc[i] / np.linalg.norm(acc[i])
		y = np.cross(z, mag[i])
		y = y / np.linalg.norm(y)
		x=np.cross(y,z)
		R = np.array([x,y,z])
		q.append(Quaternion(matrix=R))
	return q

def quatFromGyr(gyr, rate):
	q = []
	for i in range(np.size(gyr, axis=0)):
		mag = np.linalg.norm(gyr[i])
		angle = mag / rate
		axis = gyr[i] / mag
		q.append(Quaternion(axis=axis,angle=angle))
	return q

def loadData():
	"""
	dictionary:
		- f
		- N
		- s
			- pos
			- ori
			- u
			- p
		- u
			- pos
			- ori
			- u
			- p
		- f
			- pos
			- ori
			- u
			- p
	"""
	
	out = LoadedData()
	
	octave.eval('load("m_files/Recording01_A.mat");')

	#load raw data
	out.N=7479
	out.Hz = 75
	# shoulder
	i_s_acc = octave.eval("imu.shoulder.right.acc;")
	i_s_gyr = octave.eval("imu.shoulder.right.gyr;")
	i_s_mag = octave.eval("imu.shoulder.right.mag;")
	
	# upper arm
	i_u_acc = octave.eval("imu.upper_arm.right.acc;")
	i_u_gyr = octave.eval("imu.upper_arm.right.gyr;")
	i_u_mag = octave.eval("imu.upper_arm.right.mag;")

	# forearm
	i_f_acc = octave.eval("imu.forearm.right.acc;")
	i_f_gyr = octave.eval("imu.forearm.right.gyr;")
	i_f_mag = octave.eval("imu.forearm.right.mag;")

	PSH = fixNan(octave.eval("opt.shoulder.right.PSH.pos/ 1000;"))
	ASH = fixNan(octave.eval("opt.shoulder.right.ASH.pos/ 1000;"))
	Acr = fixNan(octave.eval("opt.shoulder.right.AcrLR.pos/ 1000;"))
	C7 = fixNan(octave.eval("opt.torso.C7.pos/ 1000;"))
	T8 = fixNan(octave.eval("opt.torso.T8.pos/ 1000;"))

	EM = fixNan(octave.eval("opt.upper_arm.right.EM.pos/ 1000;"))
	EL = fixNan(octave.eval("opt.upper_arm.right.EL.pos/ 1000;"))


	RS = fixNan(octave.eval("opt.forearm.right.RS.pos/ 1000;"))
	US = fixNan(octave.eval("opt.forearm.right.US.pos/ 1000;"))

	sho=((ASH+PSH)/2)
	sho_z=C7-T8
	sho_x = np.cross(sho_z, PSH - T8)
	sho_y = np.cross(sho_z, sho_x)
	sho_q=quatFromAxes(sho_x, sho_y, sho_z)

	# Where the elbow
	# x - elbowpit, y - toward EM, z - Toward AcrLR
	#center - midway between EM-EL
	elb = (EM + EL) / 2
	elb_y = EM-EL
	elb_z = sho-elb
	elb_x = np.cross(elb_y, elb_z)
	elb_y = np.cross(elb_z, elb_x)
	elb_q = quatFromAxes(elb_x, elb_y, elb_z,True) #some value nan

	# x - forwardish, y - toward us, z - from RS-US toward EM
	# center - midway betweem RS-USs
	han = (RS+US)/2
	han_z = elb-han
	han_y = np.cross(US-RS, han_z, 1)
	han_x = np.cross(han_y, han_z, 1)
	han_q = quatFromAxes(han_x, han_y, han_z)

	out.s.p = quatFromGyr(i_s_gyr, out.Hz)
	out.s.c = quatFromAccMag(i_s_acc, i_s_mag)
	out.s.pos = sho
	out.s.ori = sho_q

	out.u.p = quatFromGyr(i_u_gyr, out.Hz)
	out.u.c = quatFromAccMag(i_u_acc, i_u_mag)
	out.u.pos = elb
	out.u.ori = elb_q

	out.f.p = quatFromGyr(i_f_gyr,out.Hz)
	out.f.c = quatFromAccMag(i_f_acc, i_f_mag)
	out.f.pos = han
	out.f.ori = han_q
