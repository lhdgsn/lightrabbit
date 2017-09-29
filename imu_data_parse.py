import sys
import numpy as np
import matplotlib.pyplot as plt

# dict of measurements and corresponding numbering in input file
#dataNames = {"gps" : 1, "accel" : 3, "gyro" : 4, "magneto" : 5, "orientation" : 81, "gravity" : 83}
dataNames = {'1' : 1, '3' : 2, '4' : 3, '5' : 4, '81' : 5, '83' : 6}
M = np.empty([len(dataNames) + 1, 15000, 3])
M[:] = np.NAN

# get data file name
filename = sys.argv[-1]
if(filename == "imu_data_parse.py"):
	print("No file name included")

# open file and parse data
with open(filename, "r") as data:
	i = 0
	for line in data:
		dat = line.rstrip("\n").split(",") # remove trailing newline and split on commas
		dat = [x.strip() for x in dat] # remove unwanted spaces
		l = len(dat)
		M[0, i, 0] = dat[0] # time
		j = 1
		while(j<l):
			if(dat[j] == '8'): # skip unwanted data
				j += 2
			elif(dat[j] == '7' or dat[j] == '6'): # skip unwanted data
				j += 4
			else: # read in xyz measurements and skip to start of next entry
				M[dataNames[dat[j]], i, :] = [float(z) for z in dat[j+1:j+4]]
				j += 4
		i += 1
	M = M[:, :i, :] # remove unused array elements


# ##########################
# ###### acceleration ######
# ##########################
# t = M[0, :, [0]]
# x = M[2, :, :].T
# X = np.concatenate((t, x), axis=0)
# mask = np.isnan(X[[1], :]) # identifies elements where no measurement (NaN)
# mask = np.nonzero(mask) # creates array of indices of NaN elements
# X = np.delete(X, mask, axis=1) # removes columns where no measurement
# X[0, :] = X[0, :] - X[0, 0] # shift time to start from 0

# # define y: up/down, z: forward/back, x:left/right 

# plt.figure()

# plt.subplot(311)
# plt.plot(X[0,:], X[3,:], '.', markersize=1)
# plt.ylabel('along track (fwd/back) acceleration')

# plt.subplot(312)
# plt.plot(X[0,:], X[1,:], '.', markersize=1)
# plt.ylabel('cross track acceleration')

# plt.subplot(313)
# plt.plot(X[0,:], X[2,:], '.', markersize=1)
# plt.ylabel('up/down acceleration')

# plt.xlabel('time (s)')

# plt.show()

# #######################
# ###### gyroscope ######
# #######################
# t = M[0, :, [0]]
# x = M[3, :, :].T
# X = np.concatenate((t, x), axis=0)
# mask = np.isnan(X[[1], :]) # identifies elements where no measurement (NaN)
# mask = np.nonzero(mask) # creates array of indices of NaN elements
# X = np.delete(X, mask, axis=1) # removes columns where no measurement
# X[0, :] = X[0, :] - X[0, 0] # shift time to start from 0

# # extract data for run1 segment
# gyro_run1_mask = np.where((X[0,:] < 205.9) | (X[0,:] > 236))
# gyro_run1 = np.delete(X, gyro_run1_mask, axis=1)

# plt.figure()

# plt.subplot(311)
# plt.plot(gyro_run1[0,:], gyro_run1[1,:], '.', markersize=1) # pitch
# plt.ylabel('pitch rate (rad/s)')
# plt.ylim([-3, 2])

# plt.subplot(312)
# plt.plot(gyro_run1[0,:], gyro_run1[2,:], '.', markersize=1) # yaw
# plt.ylabel('yaw rate (rad/s)')
# plt.ylim([-3, 2])

# plt.subplot(313)
# plt.plot(gyro_run1[0,:], gyro_run1[3,:], '.', markersize=1) # roll
# plt.ylabel('roll rate (rad/s)')
# plt.ylim([-3, 2])

# plt.xlabel('time (s)')
# # plt.title('gyro measurements during run1')
# # plt.legend(['pitch', 'yaw', 'roll'])

# plt.show()


#########################
###### orientation ######
#########################
t = M[0, :, [0]]
x = M[5, :, :].T
X = np.concatenate((t, x), axis=0)
mask = np.isnan(X[[1], :]) # identifies elements where no measurement (NaN)
mask = np.nonzero(mask) # creates array of indices of NaN elements
X = np.delete(X, mask, axis=1) # removes columns where no measurement
X[0, :] = X[0, :] - X[0, 0] # shift time to start from 0
for i in range(X.shape[1]):
	if X[1,i] > 180:
		X[1,i] -= 360

# plt.plot(X[0,:], X[3,:],'.')
# plt.show()

#################################
### extract data for run1 segment
orient_run1_mask = np.where((X[0,:] < 176.0) | (X[0,:] > 200.6))
orient_run1 = np.delete(X, orient_run1_mask, axis=1)

plt.figure()
plt.subplot(311)
# initial (standing) yaw is about -17
plt.plot(orient_run1[0,:], orient_run1[1,:] + 17, '.', markersize=1) # yaw
plt.ylabel('yaw (deg)')
plt.title('orientation measurements during run1')

plt.subplot(312)
# initial (standing) pitch is about -100 (might be able to read breaths from this too)
plt.plot(orient_run1[0,:], orient_run1[2,:] + 100, '.', markersize=1) # pitch
plt.ylabel('pitch (deg)')

plt.subplot(313)
# initial (standing) roll is about 2.5
plt.plot(orient_run1[0,:], orient_run1[3,:] - 2.5, '.', markersize=1) # roll
plt.ylabel('roll (deg)')

plt.xlabel('time (s)')

#################################
### extract data for run2 segment
orient_run2_mask = np.where((X[0,:] < 205.9) | (X[0,:] > 236))
orient_run2 = np.delete(X, orient_run2_mask, axis=1)

plt.figure()
plt.subplot(311)
# initial (standing) yaw is about
plt.plot(orient_run2[0,:], orient_run2[1,:], '.', markersize=1) # yaw
plt.ylabel('yaw (deg)')
plt.title('orientation measurements during run2')

plt.subplot(312)
# initial (standing) pitch is about
plt.plot(orient_run2[0,:], orient_run2[2,:], '.', markersize=1) # pitch
plt.ylabel('pitch (deg)')

plt.subplot(313)
# initial (standing) roll is about
plt.plot(orient_run2[0,:], orient_run2[3,:], '.', markersize=1) # roll
plt.ylabel('roll (deg)')

plt.xlabel('time (s)')

plt.show()



# magnetometer

# gps

# gravity vector


# data collection sequence was: sensor stationary on table; sensor attached to body; indoor walk; pause; straight walk; pause; run with right turn; pause; run with left turn; pause; indoor walk and remove sensor
# walk: (129.9, 159.3)
# run1: (176.9, 200.6)
# run2: (205.9, 236)