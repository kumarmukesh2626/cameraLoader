import pytest
from cameraLoader.getlatestframes import CameraLoader


# video_capture = CameraLoader('./src/config/cam_config.ini')
# video_capture.start()

# url = {'camera1','video1.mp4'}

# @pytest.mark.parametrize()
# def reciveImagesSucess():
#     while True:
#         for key, value in video_capture.frame_set.items():
#             if value:
#                 frame = value[0]
#                 # do something with the frame


# @pytest.fixture(scope='module')
# def camera_loader():
#     return CameraLoader('test_config_file.txt')

# def test_load_cameras(camera_loader):
#     cameras = camera_loader.load_cameras()
#     assert len(cameras) == 2
#     assert cameras[0]['cameraID'] == 'CAM001'
#     assert cameras[1]['nfps'] == 30



def test_empty():
    assert True


# Test the CameraLoader class
class TestCameraLoader:
    # Test case for successful initialization of CameraLoader
    def test_init_success(self):
        # Initialize the CameraLoader with a valid configuration file path
        loader = CameraLoader("src/config/cam_config.ini")
        # Check that the loader object is not None
        assert loader is not None

    # Test case for initialization failure with invalid configuration file path
    # def test_init_failure(self):
    #     # Initialize the CameraLoader with an invalid configuration file path
    #     with pytest.raises(FileNotFoundError):
    #         loader = CameraLoader("non_existent_config_file.ini")

    

    # Test case for starting the frame capture thread
    def test_start(self):
        # Initialize the CameraLoader with a valid configuration file path
        loader = CameraLoader("src/config/cam_config.ini")
        # Start the frame capture thread
        loader.start()
        # Check that the thread has started
        assert loader.stopped == False

    # Test case for stopping the frame capture thread
    def test_stop(self):
        # Initialize the CameraLoader with a valid configuration file path
        loader = CameraLoader("src/config/cam_config.ini")
        # Start the frame capture thread
        loader.start()
        # Stop the frame capture thread
        loader.stop()
        # Check that the thread has stopped
        assert loader.stopped == True
