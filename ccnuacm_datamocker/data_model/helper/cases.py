from ccnuacm_datamocker.data_model.base import DataModel
import os
from ccnuacm_datamocker.common import context
import zipfile

__all__ = ["Cases"]
__author__ = "JixiangXiong"


class Cases(DataModel):
    def __init__(self, *args, **kwargs):
        zip_name = kwargs.pop("zip_name", None)
        in_type = kwargs.pop("in_type", "in")
        out_type = kwargs.pop("out_type", "out")
        super().__init__(*args, **kwargs)

        if zip_name is None:
            raise ValueError("`zip_name` must be specified.")

        self._zip_name = zip_name
        self._in_type = in_type
        self._out_type = out_type

        if not all(isinstance(x, DataModel) for x in args):
            raise ValueError(
                f"All elements in `Cases` must be DataModel, but get `{repr(args)}`."
            )
        self._cases = list(args)

    def add(self, case):
        self._cases.append(case)

    def run(self):
        std_path = context().std_path
        tmp_path = context().tmp_path
        exe_path = os.path.join(tmp_path, "std")
        cxx = context().get_compile_options("CXX")
        cxxflags = context().get_compile_options("CXXFLAGS")
        ldflags = context().get_compile_options("LDFLAGS")
        context().logger.info(f"Compiling `{std_path}`...")

        if os.path.exists(exe_path):
            os.remove(exe_path)
        if os.system(f"{cxx} -o {exe_path} {cxxflags} {ldflags} {std_path}"):
            raise ValueError(f"Failed to compile `{std_path}`.")
        context().logger.info(f"Compiling `{std_path}` succeed.")

        context().clear_output()

        for idx, case in enumerate(self._cases, 1):
            in_file = os.path.join(context().output_dir, f"{idx}.{self._in_type}")
            out_file = os.path.join(context().output_dir, f"{idx}.{self._out_type}")
            context().logger.info("Generating case: %d..." % idx)
            with open(in_file, "w") as f:
                f.write(str(case))
            context().logger.info(f"Generating infile `{in_file}` succeed.")
            if os.system(f"{exe_path} < {in_file} > {out_file}"):
                raise ValueError(f"Failed to run `{exe_path}` with `{in_file}`.")
            context().logger.info(f"Generating outfile `{out_file}` succeed.")
        context().logger.info(f"All cases generated. Start zipping `{self._zip_name}`...")

        zip_file = os.path.join(context().work_dir, self._zip_name)
        count = 0

        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(context().output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, context().output_dir))
                    count += 1

        context().logger.info(
            f"All cases zipped, result: `{zip_file}`. {len(self._cases)} cases, {count} files in total.")
