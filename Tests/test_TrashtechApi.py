import pytest
from trashtech_api import *


class TestTrashTechApi:

    def test_GetConfiguration(self):
        # Arrange
        trashtechApi = TrashtechApi()

        # Act
        configuration = trashtechApi.GetConfiguration()

        # Assert
        assert configuration is not None
