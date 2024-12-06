from plyfile import PlyData,PlyElement
import numpy as np
import open3d as o3d


path = "data/DTU/scan24/sparse/0/points3D_MVS_origin.ply"
path_trans = "data/DTU/scan24/sparse/0/points3D_MVS.ply"
plydata = PlyData.read(path)
xyz = np.stack((np.asarray(plydata.elements[0]["x"]),
                        np.asarray(plydata.elements[0]["y"]),
                        np.asarray(plydata.elements[0]["z"])), axis=1)

print("删掉黑色的点之前：",xyz.shape[0])

color = np.stack((np.asarray(plydata.elements[0]["red"]),
                        np.asarray(plydata.elements[0]["green"]),
                        np.asarray(plydata.elements[0]["blue"])), axis=1)

nxyz = np.stack((np.asarray(plydata.elements[0]["nx"]),
                        np.asarray(plydata.elements[0]["ny"]),
                        np.asarray(plydata.elements[0]["nz"])), axis=1)

color_means = np.mean(color,axis=1)
color_to_delete = np.where(color_means < 55)[0]

color = np.delete(color, color_to_delete, axis=0)
xyz = np.delete(xyz, color_to_delete, axis=0)
nxyz = np.delete(nxyz, color_to_delete, axis=0)
print("删掉黑色的点之后：",xyz.shape[0])

l = ['x', 'y', 'z', 'red', 'green', 'blue','nx','ny','nz']
dtype_full = [(attribute, 'f4') for attribute in l]

# dtype_full = [('x', 'd'), ('y', 'd'), ('z', 'd')]
# for attribute in ['red', 'green', 'blue']:
#     dtype_full += [(attribute, 'd')]  
# dtype_full += [('nx', 'd'), ('ny', 'd'), ('nz', 'd')]

elements = np.empty(xyz.shape[0], dtype=dtype_full)
attributes = np.concatenate((xyz, color,nxyz), axis=1)
elements[:] = list(map(tuple, attributes))
el = PlyElement.describe(elements, 'vertex')
PlyData([el]).write(path_trans)


pcd = o3d.io.read_point_cloud(path_trans)
voxel_size = 0.005  # 可以根据需要调整voxel_size的值
downsampled_pcd = pcd.voxel_down_sample(voxel_size)
# downsampled_pcd, indices, _ = pcd.voxel_down_sample_and_trace(
#     voxel_size=voxel_size,
#     min_bound=pcd.get_min_bound(),
#     max_bound=pcd.get_max_bound(),
#     approximate_class=False)
# downsampled_pcd.colors = pcd.colors[indices]
print("open3d下采样之后：",downsampled_pcd)


o3d.io.write_point_cloud(path_trans, downsampled_pcd)




print("end")