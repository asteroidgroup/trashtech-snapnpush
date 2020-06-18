import os.path
from Models.DeviceConfiguration import *
from trashtech_api import *
from Configuration.AppConfigurationManager import AppConfigurationManager

class DeviceConfigurationManager:
    _configFilePath: str = ''
    _deviceConfiguration: DeviceConfiguration = None
    _trashtechApi: TrashtechApi = None

    def __init__(self, trashtechApi: TrashtechApi, appConfigurationManager: AppConfigurationManager):

        if trashtechApi is None:
            raise ValueError('ConfigurationManager: Class initialization with not initialized trashtechApi')

        if appConfigurationManager is None:
            raise ValueError('ConfigurationManager: Class initialization with not initialized appConfigurationManager')

        self._configFilePath = appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath
        self._trashtechApi = trashtechApi

    def LoadFromFile(self) -> DeviceConfiguration:
        try:
            if os.path.isfile(self._configFilePath):
                with open(self._configFilePath, "rb") as configFile:
                    data = json.load(configFile)

                    self._deviceConfiguration = DeviceConfiguration(data['photo_interval'],
                                                                    data['photo_rotation'],
                                                                    data['photo_width'],
                                                                    data['photo_height'],
                                                                    data['custom_resolution'])
                    return self._deviceConfiguration
            else:
                return None
        except IOError as e:
            return None

    def TryGetDeviceConfiguration(self) -> DeviceConfiguration:

        if self._deviceConfiguration is not None:
            return self._deviceConfiguration
        else:
            localConfig = self.LoadFromFile()

            if localConfig is not None:
                self._deviceConfiguration = localConfig
                return self._deviceConfiguration
            else:
                self._deviceConfiguration = self._trashtechApi.GetConfiguration()

                if self._deviceConfiguration is None:
                    return None

                self.SaveConfiguration()
                return self._deviceConfiguration

    def SaveConfiguration(self):

        if self._deviceConfiguration is None:
            return False

        try:

            with open(self._configFilePath, 'w') as outfile:
                json.dump(self._deviceConfiguration, outfile, default=lambda o: o.__dict__)
                return True

        except Exception as e:
            return False
