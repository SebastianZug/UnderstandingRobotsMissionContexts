from dataclasses import dataclass
import numpy as np

@dataclass
class CameraParameter:
    frame: str
    delta_x : float
    delta_y : float
    delta_angle : float
    offset: float
    local_camera_max_angle: float
    local_camera_min_angle: float
    global_camera_max_angle: float
    global_camera_min_angle: float

    def __init__(self, frame, delta_x, delta_y, delta_angle, offset, 
                 local_camera_max_angle, local_camera_min_angle,
                 camera_max_angle=None, camera_min_angle=None):
        self.frame = frame
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle
        self.offset = offset
        self.local_camera_max_angle = local_camera_max_angle
        self.local_camera_min_angle = local_camera_min_angle
        if (camera_max_angle is not None) & \
           (camera_min_angle is not None):
            print("Please run transform_view_range() for checking and transforming the global view range")

    def __repr__(self):
        return f"\nCamera '{self.frame}'\n" + \
               f"delta_x={self.delta_x}, delta_y={self.delta_y}, delta_angle={self.delta_angle}\n" + \
               f"offset={self.offset} \n" + \
               f"local_camera_max_angle={self.local_camera_max_angle}, local_camera_min_angle={self.local_camera_min_angle}\n" 
    
    def transform_view_range(self, max_angle, min_angle):
        # Checking
        if self.local_camera_max_angle > max_angle:
            self.local_camera_max_angle = max_angle
        if self.local_camera_min_angle < min_angle:
            self.local_camera_min_angle = min_angle
        
        # Transforming
        self.global_camera_max_angle = self.local_camera_max_angle + self.delta_angle
        self.global_camera_min_angle = self.local_camera_min_angle + self.delta_angle
        if self.global_camera_max_angle > 180:
            self.global_camera_max_angle -= 360
        if self.global_camera_min_angle > 180:
            self.global_camera_min_angle -= 360