import os
import platform
import sys

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# os.path.join(BASE_DIR)
if platform.system() == "Windows":
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
    print(BASE_DIR)
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

sys.path.append(BASE_DIR)
from core import HouseStark

if __name__ == '__main__':
    HouseStark.ArgvHandler(sys.argv)
