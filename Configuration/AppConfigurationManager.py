from Models.AppConfiguration import AppConfiguration
import json

class AppConfigurationManager:
    appConfiguration: AppConfiguration = None

    def __init__(self):
        with open('./appconfig.json', 'rb') as appConfigurationFile:

            appConfiguration = json.load(appConfigurationFile)
            self.appConfiguration = AppConfiguration(appConfiguration['deviceConfigurationLocalFilePath'])
