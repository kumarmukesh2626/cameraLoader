'''

INFO: modular config code to fetch any config file.
By: Mukesh Algo8 AI
Date: 27-June-2022

'''
import configparser
import cv2


class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)

        for k in d:
            print(k, d[k])
            # print('{}{}'.format(k, d[k]))
        # for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


#
# config = MyParser()
# config.read("setting_config.ini")
# config_setting = config.as_dict()
#
#
#
#
#
# for cam in config_setting.keys():
# print(cam)
#    print(config_setting[cam]['designated_area'])


# config_value = configparser.ConfigParser()
#
# function to fetch config values of sections dynamically
# def read_config_file(getsections):
#    # read config file from the directory
#    config_value.read('/home/mukesh/Desktop/Scripts/stitching_feed_unavailablity/all_scripts/setting_config.ini')
#    # create list of sections available in the config file
#    list_sections  = config_value.sections()
#    # check if parsed section is in the list we of section we have
#    if getsections not in list_sections:
#        return(False,"section not found")
#    else:
#        print("found section")
#    #  create dictionary of all the values and parse it to the code
#    dict_new = {}
#    for key_config in config_value[getsections]:
#        dict_new[key_config] = config_value[getsections][key_config]
#    #  return fetched values in the code
#    return(True, dict_new)
#
# ad,sdf  = read_config_file("video")
# print(sdf['url'])
#
# for cam in sdf.values():
#        print(cam)
# camera = []
# for l in rtsp_list:
# print(l)
# camera.append(cv2.VideoCapture(cam))
# print(camera)
#
