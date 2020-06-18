import pytest
from Configuration.DeviceConfigurationManager import *
from Configuration.AppConfigurationManager import *
from trashtech_api import *


class TestConfigurationManager:

    def test_LoadFromFile_NoneTrashtechApiParameter_Invalid(self):
        with pytest.raises(Exception):
            # Arange
            trashtechApi = None

            # Act + Assert
            assert DeviceConfigurationManager(trashtechApi, None)

    def test_LoadFromFile_NoneAppConfigurationManagerParameter_Invalid(self):
        with pytest.raises(Exception):
            # Arange
            trashtechApi = TrashtechApi()
            appConfigurationManager = None

            # Act + Assert
            assert DeviceConfigurationManager(trashtechApi, appConfigurationManager)

    def test_LoadFromFile_FileDoesNotExsist_Valid(self):

        # Arange
        trashtechApi = TrashtechApi()
        appConfigurationManager = AppConfigurationManager()

        appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath = 'blabla.json'

        deviceConfigurationManager = DeviceConfigurationManager(trashtechApi, appConfigurationManager)

        # Act
        deviceConfiguration = deviceConfigurationManager.LoadFromFile()

        # assert
        assert deviceConfiguration is None

    def test_LoadFromFile_FileExsist_Valid(self):
        # Arange
        trashtechApi = TrashtechApi()
        appConfigurationManager = AppConfigurationManager()

        appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath = './Tests/Resources/DeviceConfigurationSnapshot.json'

        deviceConfigurationManager = DeviceConfigurationManager(trashtechApi, appConfigurationManager)

        # Act
        deviceConfiguration = deviceConfigurationManager.LoadFromFile()

        # assert
        assert deviceConfiguration is not None
        assert isinstance(deviceConfiguration, DeviceConfiguration)

    def test_SaveConfiguration_DeviceConfigLoaded_Valid(self):

        # Arange
        trashtechApi = TrashtechApi()
        appConfigurationManager = AppConfigurationManager()

        appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath = './Tests/Resources/DeviceConfigurationSnapshot.json'

        deviceConfigurationManager = DeviceConfigurationManager(trashtechApi, appConfigurationManager)
        deviceConfiguration = deviceConfigurationManager.LoadFromFile()

        # Act
        saveResult = deviceConfigurationManager.SaveConfiguration()

        # assert
        assert saveResult is True

    def test_SaveConfiguration_NoneDeviceConfig_Invalid(self):
            # Arange
            trashtechApi = TrashtechApi()
            appConfigurationManager = AppConfigurationManager()

            appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath = './Tests/Resources/DeviceConfigurationSnapshot.json'

            deviceConfigurationManager = DeviceConfigurationManager(trashtechApi, appConfigurationManager)

            # Act
            saveResult = deviceConfigurationManager.SaveConfiguration()

            # assert
            assert saveResult is False

    def test_TryGetDeviceConfiguration_DeviceConfigLoadedAlready_Valid(self):
        # Arange
        trashtechApi = TrashtechApi()
        appConfigurationManager = AppConfigurationManager()

        appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath = './Tests/Resources/DeviceConfigurationSnapshot.json'

        deviceConfigurationManager = DeviceConfigurationManager(trashtechApi, appConfigurationManager)
        deviceConfiguration = deviceConfigurationManager.LoadFromFile()

        # Act
        deviceConfiguration = deviceConfigurationManager.TryGetDeviceConfiguration()

        # assert
        assert deviceConfiguration is not None

    def test_TryGetDeviceConfiguration_DeviceConfigLoadedFromDisk_Valid(self):
        # Arange
        trashtechApi = TrashtechApi()
        appConfigurationManager = AppConfigurationManager()

        appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath = './Tests/Resources/DeviceConfigurationSnapshot.json'

        deviceConfigurationManager = DeviceConfigurationManager(trashtechApi, appConfigurationManager)

        # Act
        deviceConfiguration = deviceConfigurationManager.TryGetDeviceConfiguration()

        # assert
        assert deviceConfiguration is not None

    def test_TryGetDeviceConfiguration_DeviceConfigLoadedFromNetwork_Valid(self):
        # Arange
        trashtechApi = TrashtechApi()
        appConfigurationManager = AppConfigurationManager()

        appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath = './Tests/Resources/DeviceConfigurationSnapshot1.json'

        deviceConfigurationManager = DeviceConfigurationManager(trashtechApi, appConfigurationManager)

        # Act
        deviceConfiguration = deviceConfigurationManager.TryGetDeviceConfiguration()

        # assert
        assert deviceConfiguration is not None

        os.remove(appConfigurationManager.appConfiguration.deviceConfigurationLocalFilePath)
