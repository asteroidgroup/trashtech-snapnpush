

class DeviceConfiguration:

    photo_interval: int = -1
    photo_rotation: int = -1
    photo_width: int = -1
    photo_height: int = -1
    custom_resolution: bool = False

    def __init__(self,
                 photo_interval,
                 photo_rotation,
                 photo_width,
                 photo_height,
                 custom_resolution):

        self.photo_interval = photo_interval
        self.photo_rotation = photo_rotation
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.custom_resolution = custom_resolution