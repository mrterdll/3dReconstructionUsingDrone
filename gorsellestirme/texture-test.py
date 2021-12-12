import pandas
import numpy as np
import pyvista as pv

column_names = ["x","y","z","r","g","b"]
points = pandas.read_csv("sfm.ply",delimiter = " ",names=column_names)
#points.drop(points[points.z > 0.8].index, inplace=True)
#convert pandas dataframe to numpy array
numpy_arr = points[["x","y","z"]].to_numpy()

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