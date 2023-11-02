import open3d as o3d
import open3d.core as o3c
import pandas as pd
import numpy as np
import time


def pipeline(xyz, file_name=False,
             voxel_down=False, # voxel down
             remove_statistical_outliers=False, neighbors=20, std=2.0, display_inliers_outliers=False, # stat outlier
             remove_radius_outliers=False, nb_points=16, radius=0.05, # radius outlier
             estimate_normals=False, # normals
             alpha_shapes=False, alpha=0.5, # alpha surface
             ball_pivoting=False, radii=[0.005, 0.01, 0.02, 0.04], # ball pivoting
             poisson_surface=False, poisson_depth=9, # poisson surface
             smoothing=False, smoothing_iters=5, smoothing_lambda=0.5, smoothing_mu=0.5, # smoothing
             viz=False): # visualization on/off

    def change_background_to_black(vis):
        opt = vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0])
        return False

    key_to_callback = {}
    key_to_callback[ord("K")] = change_background_to_black
    
    # if no file name specified
    if not file_name:
        file_name = "Objects/PCD_visualization_" + str(time.time()).replace('.','_') + ".ply"
        
    # 1. Data conversion
    if not isinstance(xyz, str):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
    else:
        try: 
            pcd = o3d.io.read_point_cloud(xyz)
        except:
            return "Data must be either a NumPy array of (x,y,z) coordinates, or a .pcd or .ply file"
    # white_color = [255, 255, 255, 0.5]
    # colors = np.tile(white_color, (len(pcd.points), 1))
    # for i in range(len(pcd.colors)):
    #     pcd.colors[i] = white_color
    # ----------------------------------------------------------------------
    # 2. Voxel downsampling
    if voxel_down == True:
        pcd = pcd.voxel_down_sample(voxel_size=0.02)
        # write to file:
        o3d.io.write_point_cloud(file_name, pcd)
        # must read pcd file back through o3d.t
    # ----------------------------------------------------------------------
    # 3. Outlier removal
    if remove_statistical_outliers == True:
        pcd = o3d.io.read_point_cloud(file_name)  
        # must be read from o3d.t.io.read_point_cloud("file_name_here")
        cl, ind = pcd.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=std)
        o3d.io.write_point_cloud(file_name, pcd)

        if display_inliers_outliers == True:
            # function to display detected outliers in red
            def display_inlier_outlier(cloud, ind):
                inlier_cloud = cloud.select_by_index(ind)
                outlier_cloud = cloud.select_by_index(ind, invert=True)
                outlier_cloud = outlier_cloud.paint_uniform_color([1.0, 0, 0])
                inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
                inlier_cloud = o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
            pcd = o3d.io.read_point_cloud(file_name)    
            display_inlier_outlier(pcd, ind)

    if remove_radius_outliers == True:
        pcd = o3d.io.read_point_cloud(file_name)  
        # must be read from o3d.t.io.read_point_cloud("file_name_here")
        cl, ind = pcd.remove_radius_outlier(nb_points=16, radius=0.05)
        o3d.io.write_point_cloud(file_name, pcd)

        if display_inliers_outliers == True:
            # function to display detected outliers in red
            def display_inlier_outlier(cloud, ind):
                inlier_cloud = cloud.select_by_index(ind)
                outlier_cloud = cloud.select_by_index(ind, invert=True)
                outlier_cloud = outlier_cloud.paint_uniform_color([1.0, 0, 0])
                inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
                inlier_cloud = o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
            pcd = o3d.io.read_point_cloud(file_name)    
            display_inlier_outlier(pcd, ind)
    # ----------------------------------------------------------------------
    # 4. Set bounds
    # if set_bounds == True:
    #     pcd = o3d.io.read_point_cloud(file_name)  
    #     points = np.asarray(pcd.points)
    #     x_min, x_max = X[0], X[1]
    #     y_min, y_max = Y[0], Y[1]
    #     z_min, z_max = Z[0], Z[1]
    #     filtered_indices = np.where(
    #     (points[:, 0] >= x_min) & (points[:, 0] <= x_max) &
    #     (points[:, 1] >= y_min) & (points[:, 1] <= y_max) &
    #     (points[:, 2] >= z_min) & (points[:, 2] <= z_max))
    #     pcd = pcd.select_by_index(filtered_indices)
    #     o3d.io.write_point_cloud(file_name, pcd)
    # ----------------------------------------------------------------------
    # 5. Non-permanent object removal
    # ----------------------------------------------------------------------
    # 6. Triangulation of PCD
    # ----------------------------------------------------------------------
    # 7. Vertex normal estimation
    if estimate_normals == True:
        pcd = o3d.io.read_point_cloud(file_name)    
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        o3d.io.write_point_cloud(file_name, pcd)
    # ----------------------------------------------------------------------        
    # 8. Surface mesh creation
    # 8.1 Alpha shapes
    if (alpha_shapes == True) and (ball_pivoting == False) and (poisson_surface == False): 
        pcd = o3d.io.read_point_cloud(file_name)    
        tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
            pcd, alpha, tetra_mesh, pt_map)
        mesh.compute_vertex_normals()
        file_name = "triangle_mesh_" + file_name
        o3d.io.write_triangle_mesh(file_name, mesh)
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # 8.2 Ball pivoting
    elif (ball_pivoting == True) and (alpha_shapes == False) and (poisson_surface == False):
        pcd = o3d.io.read_point_cloud(file_name)    
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii))
        file_name = "triangle_mesh_" + file_name
        o3d.io.write_triangle_mesh(file_name, mesh)
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   
    # 8.3 Poisson Surface reconstruction
    elif (poisson_surface == True) and (ball_pivoting == False) and (alpha_shapes == False):
        pcd = o3d.io.read_point_cloud(file_name)    
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=poisson_depth)
        o3d.io.write_triangle_mesh(file_name, mesh)
    # ----------------------------------------------------------------------
    # 9. Smoothing
    if smoothing: 
        mesh = mesh.filter_smooth_taubin(number_of_iterations=smoothing_iters, lambda_filter=smoothing_lambda, mu=smoothing_mu)
        o3d.io.write_triangle_mesh(file_name, mesh)
    # ----------------------------------------------------------------------
    # 10. Colorization
    # ----------------------------------------------------------------------
    # 11. Visualization
    if viz == True:
        R = 1
        G = 1
        B = 0
        print(R, G, B)
        try:
            aabb = pcd.get_axis_aligned_bounding_box()
            aabb.color = (R, G, B)
            mesh.paint_uniform_color([R, G, B])
            o3d.visualization.draw_geometries_with_key_callbacks([mesh, aabb], key_to_callback)
            # o3d.visualization.draw([mesh, aabb])
        except:
            aabb = pcd.get_axis_aligned_bounding_box()
            aabb.color = (R, G, B)
            pcd.paint_uniform_color([R, G, B])
            o3d.visualization.draw_geometries_with_key_callbacks([pcd, aabb], key_to_callback)
            # o3d.visualization.draw([pcd, aabb])
            
    return file_name