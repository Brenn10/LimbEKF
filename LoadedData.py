import numpy as np
class DClass():
	def __init__(self,):
		self.pos = []
		self.ori = []
		self.p = []
		self.c = []
	def sizes(self,):
		return [np.shape(self.pos),np.shape(self.ori),np.shape(self.p),np.shape(self.u)]
class LoadedData():
	def __init__(self,):
		self.Hz = 0
		self.N = 0
		self.s = DClass()
		self.u = DClass()
		self.f = DClass()
		
	def sizes(self,):
		return [self.s.sizes(),self.u.sizes(),self.f.sizes()]