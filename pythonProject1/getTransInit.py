import math
import numpy as np
from pyntcloud import PyntCloud
import PCA1
import ICP
import draw_row

# Angle_X = 0
# Angle_Y = 0
# Angle_Z = 0
#
# matrix_X = [[1, 0, 0],
#             [0, math.cos(Angle_X), math.sin(Angle_X)],
#             [0, -math.sin(Angle_X), math.cos(Angle_X)]]
#
# matrix_Y = [[math.cos(Angle_Y), 0, -math.sin(Angle_Y)],
#             [0, 1, 0],
#             [math.sin(Angle_Y), 0, math.cos(Angle_Y)]]
#
# matrix_Z = [[math.cos(Angle_Z), math.sin(Angle_Z), 0],
#             [-math.sin(Angle_Z), math.cos(Angle_Z), 0],
#             [0, 0, 1]]
#
# matrix = np.dot(np.dot(matrix_X, matrix_Y), matrix_Z)
#
# matrix1 = [[math.cos(Angle_Z)*math.cos(Angle_Y), math.sin(Angle_Y)*math.cos(Angle_X)+math.cos(Angle_Z)*math.sin(Angle_Y)*math.sin(Angle_X), math.sin(Angle_Z)*math.sin(Angle_X)-math.cos(Angle_Z)*math.sin(Angle_Y)*math.cos(Angle_X)],
#            [-math.sin(Angle_Z)*math.cos(Angle_Y), math.cos(Angle_Z)*math.cos(Angle_X)-math.sin(Angle_Z)*math.sin(Angle_Y)*math.sin(Angle_X), math.cos(Angle_Z)*math.sin(Angle_X)+math.sin(Angle_Z)*math.sin(Angle_Y)*math.cos(Angle_X)],
#            [math.sin(Angle_Y), -math.cos(Angle_Y)*math.sin(Angle_X), math.cos(Angle_Y)*math.cos(Angle_X)]]

path1 = 'models/data7/test_tmp_model.ply'
path2 = 'models/data9/test_tmp2.ply'

point_cloud_pynt1 = PyntCloud.from_file(path1)
points1 = point_cloud_pynt1.points
w1, rows1, center1 = PCA1.PCA(points1)

point_cloud_pynt2 = PyntCloud.from_file(path2)
points2 = point_cloud_pynt2.points
w2, rows2, center2 = PCA1.PCA(points2)

# print(type(rows1))
print(rows1)
print()
# print(np.transpose(rows1))
# print()
print(rows2)
print()
# print(np.transpose(rows2))

print(np.dot(rows1, np.transpose(rows2)))
R = np.dot(rows1, np.transpose(rows2))
print(center1)
print(center2)

matrix1 = [[R[0][0], R[1][0], R[2][0], 0],
           [R[0][1], R[1][1], R[2][1], 0],
           [R[0][2], R[1][2], R[2][2], 0],
           [0, 0, 0, 1]]
matrix2 = [[R[0][0], R[0][1], R[0][2], 0],
           [R[1][0], R[1][1], R[1][2], 0],
           [R[2][0], R[2][1], R[2][2], 0],
           [0, 0, 0, 1]]
print(matrix1)

# p, q
# p = matrix * q
# p * qT = matrix * q * qT
# p * qT = matrix

draw_row.change_dly(path1, path1+"_with_row", rows1, center1)
draw_row.change_dly(path2, path2+"_with_row", rows2, center2)

source = ICP.o3d.io.read_point_cloud(path1+"_with_row", format='ply')
target = ICP.o3d.io.read_point_cloud(path2+"_with_row", format='ply')
# target2 = ICP.o3d.io.read_point_cloud('models/data10/test_tmp2.ply', format='ply')
threshold = 10
ICP.draw_registration_result(source, target, [[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
ICP.draw_registration_result(source, target, matrix1)
ICP.draw_registration_result(target, source, matrix1)
ICP.draw_registration_result(source, target, matrix2)
ICP.draw_registration_result(target, source, matrix2)