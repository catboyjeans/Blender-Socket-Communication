import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import h5py
import matplotlib.pyplot as plt
import os 


filename='test_2.mat'
directory=r'C:\Users\david\Desktop'

fullpath=os.path.join(directory,filename)

f = h5py.File(fullpath)
# print(list(f.keys()))
data_array=f['ans']

data_time=data_array[:,0]

data_x=data_array[:,1]
data_y=data_array[:,2]
data_z=data_array[:,3]

data_rot_x=data_array[:,4]
data_rot_y=data_array[:,5]
data_rot_z=data_array[:,6]

plt.figure()
plt.subplot(211)
plt.plot(data_time,data_x,data_time,data_y,data_time,data_z)
plt.subplot(212)
plt.plot(data_time,data_rot_x,data_time,data_rot_y,data_time,data_rot_z)
plt.show()