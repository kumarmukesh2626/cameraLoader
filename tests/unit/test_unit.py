import pytest
from cameraLoader.getlatestframes import CameraLoader
import unittest
import time

def test_empty():
    assert True


# # Test the CameraLoader class
# # @pytest.mark.usefixtures("driver_init")
class TestCameraLoader():
    # Test case for successful initialization of CameraLoader

    def test_init_success(self):
        # Initialize the CameraLoader with a valid configuration file path
        loader = CameraLoader("src/config/cam_config.ini")
        # Check that the loader object is not None
        assert loader is not None
    

# #     # Test case for starting the frame capture thread
#     def test_start(self):
#         # Initialize the CameraLoader with a valid configuration file path
#         loader = CameraLoader("src/config/cam_config.ini")
#         # Start the frame capture thread
#         loader.start()
#         # Check that the thread has started
#         assert loader.stopped == False

#     # Test case for stopping the frame capture thread
    def test_stop(self):
        # Initialize the CameraLoader with a valid configuration file path
        loader = CameraLoader("src/config/cam_config.ini")
        # Start the frame capture thread
        loader.start()
        # Stop the frame capture thread
        loader.stop()
        # Check that the thread has stopped
        time.sleep(1)
        assert loader.stopped == True
