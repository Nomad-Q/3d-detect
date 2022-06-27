# 实现PCA分析和法向量计算，并加载数据集中的文件进行验证

import open3d as o3d
import os
import numpy as np
from pyntcloud import PyntCloud


# 功能：计算PCA的函数
# 输入：
#     data：点云，NX3的矩阵
#     correlation：区分np的cov和corrcoef，不输入时默认为False
#     sort: 特征值排序，排序是为了其他功能方便使用，不输入时默认为True
# 输出：
#     eigenvalues：特征值
#     eigenvectors：特征向量
def PCA(data, correlation=False, sort=True):
    # 作业1
    # # 屏蔽开始
    # # axis = 0，那么输出矩阵是1行，求每一列的平均（按照每一行去求平均）；
    # # axis = 1，输出矩阵是1列，求每一行的平均（按照每一列去求平均）。
    # # 可以这么理解，axis是几，那就表明哪一维度加起来求平均。
    # n*3
    data = data.transpose()
    # 减去每一个维度的均值   X
    data = data - data.mean(axis=1, keepdims=True)
    # X^T
    data_T = data.transpose()
    H = np.matmul(data, data_T)
    # u大小为(M, M)，s大小为(M, N)，v大小为(N, N)。
    # A = u * s * v
    eigenvectors, eigenvalues, _ = np.linalg.svd(H, full_matrices=True)
    # 屏蔽结束
    if sort:
        # argsort是降序排列    [::-1]是从大到小排
        sort = eigenvalues.argsort()[::-1]
        # 从大到小排列的特征值
        eigenvalues = eigenvalues[sort]
        # 从大到小特征值对应的特征向量
        eigenvectors = eigenvectors[:, sort]

    return eigenvalues, eigenvectors


def main():
    # 指定点云路径
    # cat_index = 10 # 物体编号，范围是0-39，即对应数据集中40个物体
    # root_dir = '/Users/renqian/cloud_lesson/ModelNet40/ply_data_points' # 数据集路径
    # cat = os.listdir(root_dir)
    # filename = os.path.join(root_dir, cat[cat_index],'train', cat[cat_index]+'_0001.ply') # 默认使用第一个点云

    # 加载原始点云
    point_cloud_pynt = PyntCloud.from_file(
        "models/test1.ply")
    # point_cloud_pynt = PyntCloud.from_file("/data/home/a123/cgw/三维物体检测/数据集/ply_data_points/bench/train/bench_0010.ply")
    point_cloud_o3d = point_cloud_pynt.to_instance("open3d", mesh=False)
    o3d.visualization.draw_geometries([point_cloud_o3d])  # 显示原始点云

    # 从点云中获取点，只对点进行处理
    points = np.array(point_cloud_pynt.points)
    # n×3
    print('total points number is:', points.shape[0])

    # 作业1 用PCA分析点云主方向
    # w 特征值，特征向量
    w, v = PCA(points)
    point_cloud_vector = v[:, 1]  # 点云主方向对应的向量
    print('the main orientation of this pointcloud is: ', point_cloud_vector)

    # 三维转二维
    projected_points = np.dot(points, v[:, :2])
    ##np.vstack():在竖直方向上堆叠
    # np.hstack():在水平方向上平铺
    projected_points = np.hstack([projected_points, np.zeros((projected_points.shape[0], 1))])

    # 画出点云图像
    projected_point_cloud_o3d = o3d.geometry.PointCloud()
    projected_point_cloud_o3d.points = o3d.utility.Vector3dVector(projected_points)
    o3d.visualization.draw_geometries([projected_point_cloud_o3d])

    # 作业2 利用PCA分析进行法向量估计
    # 由于最近邻搜索是第二章的内容，所以此处允许直接调用open3d中的函数
    # 循环计算每个点的法向量
    pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_o3d)
    normals = []

    # 某一维最大减某一维最小
    cloud_range = points.max(axis=0) - points.min(axis=0)
    # dadius: set to 5% of the cloud's max range
    radius = cloud_range.max() * 0.05
    for point in point_cloud_o3d.points:
        # 数量，索引，到该点的距离
        cnt, idxs, dists = pcd_tree.search_radius_vector_3d(point, radius)
        # print("count",cnt)
        # print("dists",len(dists))
        # v:3*3 matrix
        # 求这些点的特征值和方向量
        w, v = PCA(points[idxs])
        # v[:,-1]:3*1 matrix
        # 最小特征值对应的特征向量
        normal = v[:, -1]
        normals.append(normal)
    normals = np.array(normals, dtype=np.float64)
    print("normals", normals)
    # TODO: 此处把法向量存放在了normals中
    point_cloud_o3d.normals = o3d.utility.Vector3dVector(normals)
    # o3d.visualization.draw_geometries([point_cloud_o3d])

    o3d.visualization.draw_geometries([point_cloud_o3d], "Open3D normal estimation", width=800, height=600, left=50,
                                      top=50,
                                      point_show_normal=True, mesh_show_wireframe=False,
                                      mesh_show_back_face=False)

    # # 可视化法向量的点，并存储法向量点到文件
    normal_point1 = o3d.utility.Vector3dVector(point_cloud_o3d.normals)
    normals1 = o3d.geometry.PointCloud()
    normals1.points = normal_point1
    normals1.paint_uniform_color((0, 1, 0))  # 点云法向量的点都以绿色显示
    o3d.visualization.draw_geometries([point_cloud_o3d, normals1], "Open3D noramls points", width=800, height=600, left=50, top=50,
                                      point_show_normal=False, mesh_show_wireframe=False,
                                      mesh_show_back_face=False)


if __name__ == '__main__':
    main()