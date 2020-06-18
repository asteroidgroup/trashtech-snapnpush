

class AppConfiguration:

    deviceConfigurationLocalFilePath: str = ''

    def __init__(self, deviceConfigurationLocalFilePath: str):
        self.deviceConfigurationLocalFilePath = deviceConfigurationLocalFilePath