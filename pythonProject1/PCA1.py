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
    # 1计算数据均值
    data_mean = np.mean(data, axis=0)
    # 2对数据进行去中心化
    data = data - data_mean
    print(data)
    # 3对去中心化的数据H = Ｘ'X矩阵奇异值分解，求特征值和特征向量
    ##注意ｄａｔａ中存储的格式是ＮX3,协方差矩阵描述的是各个维度之间的相关性，所以协方差矩阵大小为３ｘ3.并且协方差矩阵为对称矩阵
    ##对角线上为各个维度内的方差，非对角线上为各个维度间的方差
    # 对称矩阵分解出来的Ｕ和Ｖ是互为转置矩阵
    H = np.dot(data.T, data)
    # H = np.cov(data, rowvar=False)
    eigenvectors, eigenvalues, eigenvectors_t = np.linalg.svd(H)
    # 4对特征值和特征向量进行排序
    if sort:
        sort = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[sort]
        # U中的列向量为特征向量
        eigenvectors = eigenvectors[:, sort]

    return eigenvalues, eigenvectors


def main():
    # 加载原始点云
    point_cloud_pynt = PyntCloud.from_file("models/test1.ply")
    point_cloud_o3d = point_cloud_pynt.to_instance("open3d", mesh=False)
    o3d.visualization.draw_geometries([point_cloud_o3d],width=800,height=600)  # 显示原始点云
    # 从点云中获取点，只对点进行处理
    points = point_cloud_pynt.points
    print('total points number is:', points.shape[0])
    size = points.shape[0]
    # 用PCA分析点云主方向
    w, u = PCA(points)
    point_cloud_vector = u[:, 0]  # 点云主方向对应的向量
    print('the main orientation of this pointcloud is: ', point_cloud_vector, 'and', w[0])
    print('the second orientation of this pointcloud is:', u[:, 1])
    print('the third orientation of this pointcloud is:', u[:, 2])

    # # 循环计算每个点的法向量
    # pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_o3d)
    # normals = []
    #
    # # 1.选取一个点,搜索１０个邻近点
    # for i in range(size):
    #     [_, idx, _] = pcd_tree.search_knn_vector_3d(point_cloud_o3d.points[i], 10)
    #     k_nearest_point = np.asarray(point_cloud_o3d.points)[idx, :]  # 按照ｉｄｘ取出k个近邻点
    #     # 2.选取改点的一个邻域，计算该邻域内的点的PCA
    #     u_1, v_1 = PCA(k_nearest_point)
    #
    #     # 3.选取出特征值最小对应的特征向量作为法向量方向
    #     normals.append(v_1[:, 2])
    #
    # normals = np.array(normals, dtype=np.float64)


if __name__ == '__main__':
    main()

