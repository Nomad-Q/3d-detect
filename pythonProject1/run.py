import numpy as np

import PointCloud
import os
import reload
import PCA1
import draw_row
from pyntcloud import PyntCloud

path1 = 'models/data1/test_tmp.ply'
path2 = 'models/data1/test_tmp1.ply'
path3 = 'models/data1/test_tmp2.ply'
path4 = 'models/data1/test_tmp3.ply'

# if os.path.exists(path1):
#     os.remove(path1)
# # file = open('models/lyy.ply', 'w').close()
# pcl = PointCloud.Cloud(file=path1, depth=True)
# pcl = PointCloud.Cloud(file=path1, color=True)
# # pcl2 = PointCloud.Cloud(file=path1)


reload.load_ply(path1, path2)
reload.remove_color(path2, path3)

# PointCloud.Cloud(file=path3)

point_cloud_pynt = PyntCloud.from_file(path3)
points = point_cloud_pynt.points
w, rows, center = PCA1.PCA(points)

print(rows)
print(center)

c = []
c.append(center[0])
c.append(center[1])
c.append(center[2])
print(c)

print(np.degrees(np.arccos(np.dot(rows[0], [0,1,0]))))

draw_row.change_dly(path3, path4, rows, c)
pcl2 = PointCloud.Cloud(file=path4)
