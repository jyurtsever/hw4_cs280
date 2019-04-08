import numpy as np
import scipy.io import loadmat
import matplotlib.pyplot as plt

def main():
	#TODO: visualize matches (maybe)
	F, res_err = fundamental_matrix()
	print('Residual in f = ', res_err)
	E = K2 @ F @ K1
	# R : cell array with the possible rotation matrices of second camera
	# t : cell array of the possible translation vectors of second camera[
	R, t = find_rotation_translation(E) #TODO might need more parameters not sure
	# Find R2 and t2 from R,t such that largest number of points lie in front
	# of the image planes of the two cameras\
	P1 = K1 @ np.concatenate(np.identity(3), np.zeros(3), axis=1)
	# % the number of points in front of the image planes for all combinations	
	num_points = np.zeros((len(t), len(R))
	# % the reconstruction error for all combinations
	errs = np.full(	(len(t), len(R)), np.inf)
	for ti in range(len(t)):
		t2 = t[ti]
		for ri in range(len(R)):
			R2 = R[ri]
			P2 = K2 @ np.concatenate(R2, t2, axis=1)
			points_3d,  errs(ti, ri) = find_3d_points() #TODO might need more params
			Z1 = points_3d[:, 3]
			Z2 = R2[3, :]@points_3d.T + t2[3]
			Z2 = Z2.T
			num_points[ti, ri] = np.sum(Z2)
				


if __name__ == '__main__':
	name = 'house'	
	data_dir = '../data/' + name

	# images
	I1 = plt.imread(data_dir + '/' + name + '/1.jpg')
	I2 = plt.imread(data_dir + '/' + name + '/2.jpg')

	# K matrices
	qq = loadmat(data_dir + '/' + name + '/1_K.mat')
	K1 = qq['K']
	qq = loadmat(data_dir + '/' + name + '/2_K.mat')
	K2 = qq['K']

	# corresponding points
	matches = [x.split(' ')[1] for x in open(data_dir + '/' + name + '/_matches.txt')).readlines()] 

	# this is a N x 4 where:
	# matches(i,1:2) is a point in the first image
	# matches(i,3:4) is the corresponding point in the second image
	main()
