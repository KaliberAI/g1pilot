from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import os

# wrapper for realsense2_camera launch file
# set camera_name to d435
# set camera_namespace to /
# set rgb_camera.color_profile:=640,480,30
# set depth_module.depth_profile:=640,480,30
# set align_depth.enable to true
# set pointcloud.enable to true
# set temporal_filter.enable to true
# set hole_filling_filter.enable to true


configurable_parameters = [
    {'name': 'camera_name', 'default': 'd435', 'description': 'camera unique name'},
    {'name': 'camera_namespace', 'default': '/', 'description': 'namespace for camera'},
    {'name': 'serial_no', 'default': "''", 'description': 'choose device by serial number'},
    {'name': 'usb_port_id', 'default': "''", 'description': 'choose device by usb port id'},
    {'name': 'device_type', 'default': "''", 'description': 'choose device by type'},
    {'name': 'config_file', 'default': "''", 'description': 'yaml config file'},
    {'name': 'json_file_path', 'default': "''", 'description': 'allows advanced configuration'},
    {'name': 'initial_reset', 'default': 'false', 'description': "''"},
    {'name': 'accelerate_gpu_with_glsl', 'default': 'false', 'description': 'enable GPU acceleration with GLSL'},
    {'name': 'rosbag_filename', 'default': "''", 'description': 'A realsense bagfile to run from as a device'},
    {'name': 'rosbag_loop', 'default': 'false', 'description': 'Enable loop playback when playing a bagfile'},
    {'name': 'log_level', 'default': 'info', 'description': 'debug log level [DEBUG|INFO|WARN|ERROR|FATAL]'},
    {'name': 'output', 'default': 'screen', 'description': 'pipe node output [screen|log]'},
    {'name': 'enable_color', 'default': 'true', 'description': 'enable color stream'},
    {'name': 'rgb_camera.color_profile', 'default': '640,480,30', 'description': 'color stream profile'},
    {'name': 'rgb_camera.color_format', 'default': 'RGB8', 'description': 'color stream format'},
    {'name': 'rgb_camera.enable_auto_exposure', 'default': 'true', 'description': 'enable/disable auto exposure for color image'},
    {'name': 'enable_depth', 'default': 'true', 'description': 'enable depth stream'},
    {'name': 'enable_infra', 'default': 'false', 'description': 'enable infra0 stream'},
    {'name': 'enable_infra1', 'default': 'false', 'description': 'enable infra1 stream'},
    {'name': 'enable_infra2', 'default': 'false', 'description': 'enable infra2 stream'},
    {'name': 'depth_module.depth_profile', 'default': '640,480,30', 'description': 'depth stream profile'},
    {'name': 'depth_module.depth_format', 'default': 'Z16', 'description': 'depth stream format'},
    {'name': 'depth_module.infra_profile', 'default': '0,0,0', 'description': 'infra streams (0/1/2) profile'},
    {'name': 'depth_module.infra_format', 'default': 'RGB8', 'description': 'infra0 stream format'},
    {'name': 'depth_module.infra1_format', 'default': 'Y8', 'description': 'infra1 stream format'},
    {'name': 'depth_module.infra2_format', 'default': 'Y8', 'description': 'infra2 stream format'},
    {'name': 'depth_module.color_profile', 'default': '0,0,0', 'description': 'Depth module color stream profile for d405'},
    {'name': 'depth_module.color_format', 'default': 'RGB8', 'description': 'color stream format for d405'},
    {'name': 'depth_module.exposure', 'default': '8500', 'description': 'Depth module manual exposure value'},
    {'name': 'depth_module.gain', 'default': '16', 'description': 'Depth module manual gain value'},
    {'name': 'depth_module.hdr_enabled', 'default': 'false', 'description': 'Depth module hdr enablement flag. Used for hdr_merge filter'},
    {'name': 'depth_module.enable_auto_exposure', 'default': 'true', 'description': 'enable/disable auto exposure for depth image'},
    {'name': 'depth_module.exposure.1', 'default': '7500', 'description': 'Depth module first exposure value. Used for hdr_merge filter'},
    {'name': 'depth_module.gain.1', 'default': '16', 'description': 'Depth module first gain value. Used for hdr_merge filter'},
    {'name': 'depth_module.exposure.2', 'default': '1', 'description': 'Depth module second exposure value. Used for hdr_merge filter'},
    {'name': 'depth_module.gain.2', 'default': '16', 'description': 'Depth module second gain value. Used for hdr_merge filter'},
    {'name': 'enable_sync', 'default': 'false', 'description': "'enable sync mode'"},
    {'name': 'depth_module.inter_cam_sync_mode', 'default': '0', 'description': '[0-Default, 1-Master, 2-Slave]'},
    {'name': 'enable_rgbd', 'default': 'false', 'description': "'enable rgbd topic'"},
    {'name': 'enable_gyro', 'default': 'false', 'description': "'enable gyro stream'"},
    {'name': 'enable_accel', 'default': 'false', 'description': "'enable accel stream'"},
    {'name': 'enable_motion', 'default': 'false', 'description': "'enable motion stream (IMU) for DDS devices'"},
    {'name': 'gyro_fps', 'default': '0', 'description': "''"},
    {'name': 'accel_fps', 'default': '0', 'description': "''"},
    {'name': 'motion_fps', 'default': '0', 'description': "'motion stream samples per second'"},
    {'name': 'unite_imu_method', 'default': '0', 'description': '[0-None, 1-copy, 2-linear_interpolation]'},
    {'name': 'clip_distance', 'default': '-2.', 'description': "''"},
    {'name': 'angular_velocity_cov', 'default': '0.01', 'description': "''"},
    {'name': 'linear_accel_cov', 'default': '0.01', 'description': "''"},
    {'name': 'diagnostics_period', 'default': '0.0', 'description': 'Rate of publishing diagnostics. 0=Disabled'},
    {'name': 'publish_tf', 'default': 'true', 'description': '[bool] enable/disable publishing static & dynamic TF'},
    {'name': 'tf_publish_rate', 'default': '0.0', 'description': '[double] rate in Hz for publishing dynamic TF'},
    {'name': 'pointcloud.enable', 'default': 'false', 'description': ''},
    {'name': 'pointcloud.stream_filter', 'default': '2', 'description': 'texture stream for pointcloud'},
    {'name': 'pointcloud.stream_index_filter', 'default': '0', 'description': 'texture stream index for pointcloud'},
    {'name': 'pointcloud.ordered_pc', 'default': 'false', 'description': ''},
    {'name': 'pointcloud.allow_no_texture_points', 'default': 'false', 'description': "''"},
    {'name': 'align_depth.enable', 'default': 'false', 'description': 'enable align depth filter'},
    {'name': 'colorizer.enable', 'default': 'false', 'description': 'enable colorizer filter'},
    {'name': 'decimation_filter.enable', 'default': 'false', 'description': 'enable_decimation_filter'},
    {'name': 'rotation_filter.enable', 'default': 'false', 'description': 'enable rotation filter'},
    {'name': 'rotation_filter.rotation', 'default': '0.0', 'description': 'rotation value: 0.0, 90.0, -90.0, 180.0'},
    {'name': 'spatial_filter.enable', 'default': 'false', 'description': 'enable_spatial_filter'},
    {'name': 'temporal_filter.enable', 'default': 'true', 'description': 'enable_temporal_filter'},
    {'name': 'disparity_filter.enable', 'default': 'false', 'description': 'enable_disparity_filter'},
    {'name': 'hole_filling_filter.enable', 'default': 'true', 'description': 'enable_hole_filling_filter'},
    {'name': 'hdr_merge.enable', 'default': 'false', 'description': 'hdr_merge filter enablement flag'},
    {'name': 'wait_for_device_timeout', 'default': '-1.', 'description': 'Timeout for waiting for device to connect (Seconds)'},
    {'name': 'reconnect_timeout', 'default': '6.', 'description': 'Timeout(seconds) between consequtive reconnection attempts'},
    {'name': 'base_frame_id', 'default': 'link', 'description': 'Root frame of the sensors transform tree'},
    {'name': 'tf_prefix', 'default': '', 'description': 'prefix to be prepended to all frame IDs'},
    {'name': 'decimation_filter.filter_magnitude', 'default': '2', 'description': 'decimation filter magnitude'},
    {'name': 'enable_safety', 'default': 'false', 'description': "'enable safety stream'"},
    {'name': 'safety_camera.safety_mode', 'default': '0', 'description': '[int] 0-Run, 1-Standby, 2-Service'},
    {'name': 'enable_labeled_point_cloud', 'default': 'false', 'description': "'enable labeled point cloud stream'"},
    {'name': 'depth_mapping_camera.labeled_point_cloud_profile', 'default': '0,0,0', 'description': "'Label PointCloud stream profile'"},
    {'name': 'enable_occupancy', 'default': 'false', 'description': "'enable occupancy stream'"},
    {'name': 'depth_mapping_camera.occupancy_profile', 'default': '0,0,0', 'description': "'Occupancy stream profile'"},
]

def generate_launch_description():
    rs_launch = os.path.join(
        get_package_share_directory('realsense2_camera'),
        'launch',
        'rs_launch.py',
    )

    launch_args = {
        param['name']: LaunchConfiguration(param['name'])
        for param in configurable_parameters
    }

    return LaunchDescription([
        *[
            DeclareLaunchArgument(
                param['name'],
                default_value=param['default'],
                description=param['description'],
            )
            for param in configurable_parameters
        ],
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rs_launch),
            launch_arguments=launch_args.items(),
        ),
    ])
