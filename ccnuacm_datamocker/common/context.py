from .project_logger import get_logger
from .random_generator import RandomGenerator
import shutil
import os

__all__ = ["context"]
__author__ = "JixiangXiong"


class DMContext:
    _ctx = {}

    def __init__(self, **kwargs):
        self._logger = get_logger()
        self._name = kwargs["name"]
        self._logger.debug(
            f"Initializing DMContext(`{self._name}`) with args: {kwargs}."
        )
        self._random_generator = RandomGenerator(seed=kwargs.get("seed", 0))
        self._work_dir = kwargs.get("work_dir", ".")
        self._std_path = kwargs.get("std_path", None)
        self._CC = kwargs.get("CC", "gcc")
        self._CXX = kwargs.get("CXX", "g++")
        self._CFLAGS = kwargs.get("CFLAGS", "")
        self._CXXFLAGS = kwargs.get("CXXFLAGS", "-O2 -std=c++17")
        self._LDFLAGS = kwargs.get("LDFLAGS", "")

    @classmethod
    def get_context(cls, name="default", **kwargs):
        if cls._ctx.get(name) is None:
            cls._ctx[name] = DMContext(name=name, **kwargs)
        return cls._ctx[name]

    @property
    def logger(self):
        if self._logger is None:
            raise ValueError(f"Logger of DMContext(`{self._name}`) is not initialized.")
        return self._logger

    @property
    def random(self) -> RandomGenerator:
        if self._random_generator is None:
            raise ValueError(f"RandomGenerator of DMContext(`{self._name}`) is not initialized.")
        return self._random_generator

    @property
    def work_dir(self):
        work_dir_ = self._work_dir
        if not os.path.exists(work_dir_):
            self.logger.info(f"Creating work directory `{work_dir_}`.")
            os.makedirs(work_dir_)
        return work_dir_

    @property
    def output_dir(self):
        output_dir_ = os.path.join(self.work_dir, "output")
        if not os.path.exists(output_dir_):
            self.logger.info(f"Creating output directory `{output_dir_}`.")
            os.makedirs(output_dir_)
        return output_dir_

    @work_dir.setter
    def work_dir(self, path):
        if not isinstance(path, str):
            raise ValueError(f"Invalid work_dir: `{path}`, str expected.")
        self._work_dir = path

    @property
    def std_path(self):
        if self._std_path is None:
            std_path_ = os.path.join(self.work_dir, "std.cpp")
            if os.path.exists(std_path_):
                self._std_path = std_path_
                self.logger.info(f"Using `{std_path_}` as standard solution by default, or you can use "
                                 f"`ccnuacm_datamocker.set_std_path` to modify it.")
            else:
                raise ValueError(f"Cannot find standard solution not found in `{std_path_}`, you can move your "
                                 f"solution here or use `ccnuacm_datamocker.set_std_path` to set the path. BTW, "
                                 f"pwd path is {os.getcwd()}.")
        else:
            if not os.path.exists(self._std_path):
                raise ValueError(f"Standard solution not found in `{self._std_path}`, you can move your solution here "
                                 f"or use `ccnuacm_datamocker.set_std_path` to set the path. BTW, pwd path is "
                                 f"{os.getcwd()}.")
        return self._std_path

    @property
    def tmp_path(self):
        tmp_path_ = os.path.join(self.work_dir, "tmp")
        if not os.path.exists(tmp_path_):
            self.logger.info(f"Creating tmp directory `{tmp_path_}`.")
            os.makedirs(tmp_path_)
        return tmp_path_

    @std_path.setter
    def std_path(self, path: str):
        path = path.strip()
        if path == "":
            raise ValueError("Empty path is not allowed.")
        if len(path) >= 2 and path[:2] == '$/':
            path = os.path.join(self.work_dir, path[2:])
        if not os.path.exists(path):
            raise ValueError(f"Standard solution not found in `{path}`, you can move your solution here or use "
                             f"`ccnuacm_datamocker.set_std_path` to set the path. BTW, pwd path is {os.getcwd()}.")
        self._std_path = path

    def clear_output(self):
        output_dir = self.output_dir
        context().logger.info(f"Clearing output directory `{output_dir}`.")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    def set_compile_options(self, *, CC=None, CXX=None, CFLAGS=None, CXXFLAGS=None, LDFLAGS=None):
        if CC is not None:
            self._CC = CC
        if CXX is not None:
            self._CXX = CXX
        if CFLAGS is not None:
            self._CFLAGS = CFLAGS
        if CXXFLAGS is not None:
            self._CXXFLAGS = CXXFLAGS
        if LDFLAGS is not None:
            self._LDFLAGS = LDFLAGS

    def get_compile_options(self, name):
        if name == "CC":
            return self._CC
        if name == "CXX":
            return self._CXX
        if name == "CFLAGS":
            return self._CFLAGS
        if name == "CXXFLAGS":
            return self._CXXFLAGS
        if name == "LDFLAGS":
            return self._LDFLAGS
        raise ValueError(f"Invalid compile option name: `{name}`.")


def context(**kwargs) -> DMContext:
    return DMContext.get_context(**kwargs)
