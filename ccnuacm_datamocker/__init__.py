__all__ = ["set_seed", "set_work_dir", "set_std_path", "clear_output"]
__author__ = "JixiangXiong"


def set_seed(seed_):
    from .common import context
    context().random.set_seed(seed_)


def set_work_dir(work_dir):
    from .common import context
    context().work_dir = work_dir


def set_std_path(path):
    from .common import context
    context().std_path = path


def clear_output():
    from .common import context
    context().clear_output()
