import platform
from glob import glob
import os.path

from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup, find_packages


IS_WIN = platform.system() == "Windows"
__version__ = "0.0.1"


def get_libraries():
    libraries = ["rocksdb", "lz4", "snappy"]
    if IS_WIN:
        libraries.extend(["Rpcrt4", "Shlwapi"]) # for port_win.cc
        libraries.extend(["zlibstatic", "zstd_static"])
        libraries.append("Cabinet") # for XPRESS
    else:
        libraries.extend(["bz2", "z", "zstd"])
    return libraries


ext_m = Pybind11Extension(
    "rocksdb_python",
    sorted(glob("src/*.cpp")),
    include_dirs=["rocksdb/include"],
    libraries=get_libraries(),
    library_dirs=["."],
    runtime_library_dirs = [os.path.abspath("/opt/homebrew/opt/lz4/lib"),
                            os.path.abspath("/opt/homebrew/opt/snappy/lib"),
                            os.path.abspath("/opt/homebrew/opt/bzip2/lib"),
                            os.path.abspath("/opt/homebrew/opt/zlib/lib"),
                            os.path.abspath("/opt/homebrew/opt/zstd/lib")],
    define_macros=[("VERSION_INFO", __version__)],
    cxx_std=17,
)
ext_modules = [ext_m]

setup(
    name="rocksdb-python",
    version=__version__,
    ext_modules=ext_modules,
    packages=find_packages(exclude=['test']),
)
