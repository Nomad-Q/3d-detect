from mayavi import mlab
import numpy as np
import open3d as o3d
import copy


def ply_read(file_path):
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines


# 将每一行数据分割后转为数字
def ls2n(line):
    line = line.strip().split(' ')
    return list(map(float, line))


def viz_mayavi_3(points1, points2, points3):
    x = points1[:, 0]  # x position   of point
    y = points1[:, 1]  # y position   of point
    z = points1[:, 2]  # z position   of point
    fig = mlab.figure(bgcolor=(0, 0, 0), size=(640, 360))
    mlab.points3d(x, y, z, z, mode="point", color=(0, 1, 0), figure=fig)

    x = points2[:, 0]  # x position   of point
    y = points2[:, 1]  # y position   of point
    z = points2[:, 2]  # z position   of point
    mlab.points3d(x, y, z, z, mode="point", color=(1, 0, 0), figure=fig)

    x = points1[:, 0]  # x position   of point
    y = points1[:, 1]  # y position   of point
    z = points1[:, 2]  # z position   of point
    mlab.points3d(x, y, z, z, mode="point", color=(0, 0, 1), figure=fig)

    mlab.show()

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


if __name__ == '__main__':
    # # file_path = 'bun000.ply'
    # file_path = 'models/data1/test_tmp2.ply'
    # points = ply_read(file_path)
    # points = points[24:(24 + 40256)]
    # points1 = np.array(list(map(lambda x: ls2n(x), points)))
    #
    # # file_path = 'bun045.ply'
    # file_path = 'models/data2/test_tmp2.ply'
    # points = ply_read(file_path)
    # points = points[24:(24 + 40097)]
    # points2 = np.array(list(map(lambda x: ls2n(x), points)))
    #
    # threshold = 0.2  # 距离阈值
    # trans_init = np.array([[1.0, 0.0, 0.0, 0.0],
    #                        [0.0, 1.0, 0.0, 0.0],
    #                        [0.0, 0.0, 1.0, 0],
    #                        [0.0, 0.0, 0.0, 1.0]])
    # # 计算两个重要指标，fitness计算重叠区域（内点对应关系/目标点数）。越高越好。
    # # inlier_rmse计算所有内在对应关系的均方根误差RMSE。越低越好。
    # source = o3d.geometry.PointCloud()
    # source.points = o3d.utility.Vector3dVector(points1)
    # target = o3d.geometry.PointCloud()
    # target.points = o3d.utility.Vector3dVector(points2)
    # print("Initial alignment")
    # print(source)
    # icp = o3d.registration_icp(
    #     source, target, threshold, trans_init,
    #     o3d.TransformationEstimationPointToPoint())
    # print(icp)
    # source.transform(icp.transformation)
    # print(icp.transformation)
    # points3 = np.array(source.points)
    # viz_mayavi_3(points1, points2, points3)





    # demo_icp_pcds = o3d.data.DemoICPPointClouds()
    source = o3d.io.read_point_cloud('models/data1/test_tmp2.ply', format='ply')
    target = o3d.io.read_point_cloud('models/data2/test_tmp2.ply', format='ply')
    threshold = 0.02
    trans_init = np.asarray([[0.862, 0.011, -0.507, 0.5],
                             [-0.139, 0.967, -0.215, 0.7],
                             [0.487, 0.255, 0.835, -1.4],
                             [0.0, 0.0, 0.0, 1.0]])
    draw_registration_result(source, target, trans_init)

    print("Initial alignment")
    evaluation = o3d.registration.evaluate_registration(
        source, target, threshold, trans_init)
    print(evaluation)

    reg_p2p = o3d.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.registration.TransformationEstimationPointToPoint(),
        o3d.registration.ICPConvergenceCriteria(max_iteration=2000))
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    draw_registration_result(source, target, reg_p2p.transformation)