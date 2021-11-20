import pandas
import numpy as np
import pyvista as pv

column_names = ["x","y","z"]
points = pandas.read_csv("kosegen_2.asc",delimiter = " ",names=column_names)
points.drop(points[points.z > 0.8].index, inplace=True)
#convert pandas dataframe to numpy array
numpy_arr = points.to_numpy()

#clouds = pv.UnstructuredGrid(numpy_arr)

cloud = pv.PolyData(numpy_arr)
cloud.plot()

#volume = clouds.reconstruct_surface()
# volume = cloud.delaunay_3d(alpha=2.)
# shell = volume.extract_geometry()
# shell.plot()
