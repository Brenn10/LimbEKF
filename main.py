import loadData
import qEKF
from pyquaternion import Quaternion
m = loadData.loadData()

fused=qEKF.fuse(m.s.p,m.s.c,Quaternion(1,0,0,0))