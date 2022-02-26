import pandas
import numpy as np
import pyvista as pv

#function to read csv file with delimiter without library 
def read_csv(file_name, delimiter):
    with open(file_name, 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [x.split(delimiter) for x in content]
    return content
    



column_names = ["x","y","z","r","g","b"]

x = read_csv("sfm.ply", " ")

#convert x to pandas dataframe
df = pandas.DataFrame(x, columns=column_names)

numpy_arr = df[["x","y","z"]].to_numpy(dtype=np.float64)

lidar_points = pandas.read_csv("icp_lidar_mahalle.asc", delimiter=" ",names=["x","y","z"])
lidar_numpy_arr = lidar_points[["x","y","z"]].to_numpy(dtype=np.float64)
#merge two numpy arrays
numpy_arr = np.concatenate((numpy_arr,lidar_numpy_arr),axis=0)

#points = pandas.read_csv("sfm.ply",delimiter = " ",names=column_names)
#points.drop(points[points.z > 0.8].index, inplace=True)
#convert pandas dataframe to numpy array
#numpy_arr = points[["x","y","z"]].to_numpy()

#sample  = 10
#numpy_arr = numpy_arr[::sample]
#clouds = pv.UnstructuredGrid(numpy_arr)


# sphere_points = pv.Sphere().points
# points = pv.wrap(sphere_points)
# surf = points.reconstruct_surface()



#cloud = pv.PolyData(numpy_arr)
cloud = pv.wrap(numpy_arr)
cloud.plot()

volume = cloud.reconstruct_surface()
volume.plot()
# volume = cloud.delaunay_3d(alpha=2.)
# shell = volume.extract_geometry()
# shell.plot()
print("end of program")