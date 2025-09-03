import open3d as o3d

def main(pcd_file):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(pcd_file)
    
    # Downsample to approximately 1/10th the points (adjust the sampling_ratio as needed to hit ~50MB)
    # This keeps the downsampling in memory without saving or overwriting the original file
    pcd_down = pcd.random_down_sample(sampling_ratio=0.1)
    
    # Alternatively, use voxel downsampling (better for spatial uniformity; adjust voxel_size based on your point cloud's scale)
    # pcd_down = pcd.voxel_down_sample(voxel_size=0.05)  # Example: increase voxel_size for more aggressive downsampling
    
    # Visualize the downsampled version
    o3d.visualization.draw_geometries([pcd_down])

if __name__ == "__main__":
    pcd_file = 'poses_points.pcd'
    main(pcd_file)
