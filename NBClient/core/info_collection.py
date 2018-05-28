import platform
import sys

from plugins import plugin_api


class InfoCollection(object):
    def __init__(self):
        pass

    def collect(self):
        os_platform = self.get_platform()
        try:
            func = getattr(self, os_platform)
            info_data = func()
            formatted_data = self.build_report_data(info_data)
            return formatted_data
        except Exception as e:
            sys.exit("error:Mark doens't support os [%s]!" % os_platform)

    def Linux(self):
        sys_info = plugin_api.LinuxSysInfo()
        return sys_info

    def Windows(self):
        sys_info = plugin_api.WindowsSysInfo()
        return sys_info

    def get_platform(self):
        os_platform = platform.system()
        return os_platform

    def build_report_data(self, data):
        return data
