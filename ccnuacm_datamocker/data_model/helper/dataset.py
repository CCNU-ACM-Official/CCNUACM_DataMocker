import subprocess

from ccnuacm_datamocker.data_model.base import DataModel
import os
from ccnuacm_datamocker.common import context
import zipfile
from tqdm import tqdm

__all__ = ["DataSet"]
__author__ = "JixiangXiong"


class DataSet(DataModel):
    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        std_path = kwargs.pop("std_path", None)
        in_type = kwargs.pop("in_type", "in")
        out_type = kwargs.pop("out_type", "out")
        seed = kwargs.pop("seed", context().seed)
        super().__init__(*args, **kwargs)

        if std_path is None:
            raise ValueError("`std_path` must be specified.")
        if name is None:
            name = os.path.basename(std_path)

        path = std_path
        if path == "":
            raise ValueError("Empty path is not allowed.")
        if len(path) >= 2 and path[:2] == "$/":
            path = os.path.join(context().std_dir, path[2:])
        if not os.path.exists(path):
            raise ValueError(
                f"Standard solution not found in `{path}`, you can move your solution here or use"
                f" `std_path` to set the path. BTW, pwd path is {os.getcwd()}."
            )
        self._std_path = os.path.abspath(path)

        self._zip_file = name + ".zip"
        self._zip_name = name
        self._dir = os.path.join(context().tmp_dir, self._zip_name)
        self._in_type = in_type
        self._out_type = out_type
        self._seed = seed

        if not all(isinstance(x, DataModel) for x in args):
            raise ValueError(
                f"All elements in `Cases` must be DataModel, but get `{repr(args)}`."
            )
        self._cases = list(args)

    def add(self, *cases, **kwargs):
        repetation = kwargs.get("repetation", 1)
        for c in cases:
            if isinstance(c, list | tuple):
                for cc in c:
                    if not isinstance(cc, DataModel):
                        raise ValueError(
                            f"All elements in `Cases` must be DataModel, but get `{repr(cc)}`."
                        )
                    for _ in range(repetation):
                        self._cases.append(cc)
                continue
            if not isinstance(c, DataModel):
                raise ValueError(
                    f"All elements in `Cases` must be DataModel, but get `{repr(c)}`."
                )
            for _ in range(repetation):
                self._cases.append(c)

    def run(self):
        std_path = self.std_path
        exe_path = os.path.join(context().exec_dir, self._zip_name + ".exe")
        out_dir = self._dir
        cxx = context().get_compile_options("CXX")
        cxxflags = context().get_compile_options("CXXFLAGS")
        ldflags = context().get_compile_options("LDFLAGS")

        if os.path.exists(exe_path):
            os.remove(exe_path)
        context().logger.info(
            f"Compiling `{std_path}` with command: `{cxx} -o {exe_path} {cxxflags} {ldflags} {std_path}`."
        )
        compile_result = subprocess.run(
            f"{cxx} -o {exe_path} -O2 -std=c++17 {cxxflags} {ldflags} {std_path}",
            capture_output=True,
        )
        if compile_result.returncode:
            raise ValueError(
                f'Failed to compile `{std_path}`.\nerrmsg:\n{compile_result.stdout.decode("utf-8")}\n'
                f'{compile_result.stderr.decode("utf-8")}'
            )
        context().logger.info(f"Compiling `{std_path}` succeed.")

        context().clear_dir(out_dir)
        context().make_dir(out_dir)
        context().seed = self._seed

        context().logger.info("Start generating cases...")

        t = tqdm(
            enumerate(self._cases, 1), desc="Generating cases", total=len(self._cases)
        )
        for idx, case in t:
            t.set_description(f"Generating case #{idx}")
            in_file = os.path.join(out_dir, f"{idx}.{self._in_type}")
            out_file = os.path.join(out_dir, f"{idx}.{self._out_type}")
            context().logger.debug("Generating case #%d..." % idx)
            with open(in_file, "w") as f:
                f.write(str(case) + "\n")
            context().logger.debug(f"Generating infile `{in_file}` succeed.")
            context().logger.debug(
                f"Generating outfile using command: `{exe_path} < {in_file} > {out_file}`."
            )
            exec_result = subprocess.run(
                exe_path,
                stdin=open(in_file),
                stdout=open(out_file, "w"),
            )
            if exec_result.returncode:
                raise ValueError(
                    f"Failed to exec command: `{exe_path} < {in_file} > {out_file}`.\nerrmsg:\n"
                    f'{exec_result.stdout.decode("utf-8")}\n{exec_result.stderr.decode("utf-8")}'
                )
            context().logger.debug(f"Generating outfile `{out_file}` succeed.")
        context().logger.info(
            f"All cases generated. Start zipping `{self._zip_name}.zip`..."
        )

        zip_file = os.path.join(context().zip_dir, self._zip_name + ".zip")
        count = 0

        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(out_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, out_dir))
                    count += 1

        context().logger.info(
            f"All cases zipped, result: `{zip_file}`. {len(self._cases)} cases, {count} files in total."
        )

    @property
    def std_path(self):
        if not os.path.exists(self._std_path):
            raise ValueError(
                f"Standard solution not found in `{self._std_path}`, you can move your solution here "
                f"or use `ccnuacm_datamocker.set_std_path` to set the path. BTW, pwd path is "
                f"{os.getcwd()}."
            )
        return self._std_path

    def brief(self):
        result = f"DataSet: {self._zip_name}, brief:\n"
        length = len(self._cases)
        if length == 0:
            return result + "Dataset Empty."
        if length > 5:
            return (
                result
                + "\n".join(
                    f"\nCase #{idx + 1}:\n" + x.brief()
                    for idx, x in enumerate(self._cases[:5])
                )
                + "\n..."
            )
        return result + "\n".join(
            f"\nCase #{idx + 1}:\n" + x.brief() for idx, x in enumerate(self._cases)
        )
