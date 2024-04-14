from .project_logger import get_logger
from .random_generator import RandomGenerator
import shutil
import os
import subprocess

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
        self._CC = kwargs.get("CC", "gcc")
        self._CXX = kwargs.get("CXX", "g++")
        self._CFLAGS = kwargs.get("CFLAGS", "")
        self._CXXFLAGS = kwargs.get("CXXFLAGS", "-O2 -std=c++17")
        self._LDFLAGS = kwargs.get("LDFLAGS", "")
        self._seed = kwargs.get("seed", 0)
        self._work_dataset = None

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
            raise ValueError(
                f"RandomGenerator of DMContext(`{self._name}`) is not initialized."
            )
        return self._random_generator

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = seed
        self._random_generator.seed = seed

    @property
    def work_dir(self):
        work_dir_ = self._work_dir
        if not os.path.exists(work_dir_):
            self.logger.info(f"Creating work directory `{work_dir_}`.")
            os.makedirs(work_dir_)
        return work_dir_

    @property
    def std_dir(self):
        std_dir_ = os.path.join(self.work_dir, "std")
        if not os.path.exists(std_dir_):
            self.logger.info(f"Creating work directory `{std_dir_}`.")
            os.makedirs(std_dir_)
        return std_dir_

    @property
    def tmp_dir(self):
        tmp_dir_ = os.path.join(self.work_dir, "tmp")
        if not os.path.exists(tmp_dir_):
            self.logger.info(f"Creating output directory `{tmp_dir_}`.")
            os.makedirs(tmp_dir_)
        return tmp_dir_

    @work_dir.setter
    def work_dir(self, path):
        if not isinstance(path, str):
            raise ValueError(f"Invalid work_dir: `{path}`, str expected.")
        context().logger.info(f"Setting work directory to `{os.path.abspath(path)}`.")
        self._work_dir = os.path.abspath(path)

    @property
    def zip_dir(self):
        zip_dir_ = os.path.join(self.work_dir, "zip")
        if not os.path.exists(zip_dir_):
            self.logger.info(f"Creating zip directory `{zip_dir_}`.")
            os.makedirs(zip_dir_)
        return zip_dir_

    @property
    def exec_dir(self):
        exec_dir_ = os.path.join(self.work_dir, "exec")
        if not os.path.exists(exec_dir_):
            self.logger.info(f"Creating tmp directory `{exec_dir_}`.")
            os.makedirs(exec_dir_)
        return exec_dir_

    @property
    def CXX(self):
        return self._CXX

    @CXX.setter
    def CXX(self, path):
        context().logger.info(f"Setting CXX to `{path}`.")
        result = subprocess.run([path, "-dumpversion"], capture_output=True)
        if result.returncode != 0:
            raise ValueError(
                f'Invalid compiler path: `{path}`. Failed to get version. Errmsg:\n{result.stdout.decode("utf-8")}\n'
                f'{result.stderr.decode("utf-8")}'
            )
        context().logger.info(
            f'compiler version: {result.stdout.decode("utf-8").strip()}'
        )
        self._CXX = path

    def clear_tmp(self):
        self.clear_dir(self.tmp_dir)

    @classmethod
    def clear_dir(cls, path):
        context().logger.info(f"Clearing directory `{path}`.")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    @classmethod
    def make_dir(cls, path):
        if not os.path.exists(path):
            context().logger.info(f"Creating directory `{path}`.")
            os.makedirs(path)

    def set_compile_options(
        self, *, CC=None, CXX=None, CFLAGS=None, CXXFLAGS=None, LDFLAGS=None
    ):
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
