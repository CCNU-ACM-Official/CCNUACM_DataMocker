import numpy as np


class RandomGenerator:
    def __init__(self, seed=0):
        self._random_generator: np.random.RandomState = np.random.RandomState(seed=seed)

    def set_seed(self, seed: int):
        self._random_generator.seed(seed=seed)

    def randint(self, *ranges, dtype=None) -> int:
        """
        Generate a random integer in the range [leftmost, rightmost).
        :param ranges: A single integer or two integers.
        :return: A random integer in the range [leftmost, rightmost).
        """
        if len(ranges) == 1:
            leftmost, rightmost = 0, ranges[0]
        elif len(ranges) == 2:
            leftmost, rightmost = ranges
        else:
            raise ValueError(
                f"Invalid ranges `{ranges}`, number of arguments should be 1 or 2, but given {len(ranges)}."
            )
        if leftmost >= rightmost:
            raise ValueError(
                f"Invalid range, leftmost=`{leftmost}`, rightmost=`{rightmost}`."
            )
        if dtype is None:
            dtype = np.int64
        return self._random_generator.randint(leftmost, rightmost, dtype=dtype)

    def randfloat(self, *ranges) -> float:
        """
        Generate a random float in the range [leftmost, rightmost).
        :param ranges: A single float or two floats.
        :return: A random float in the range [leftmost, rightmost).
        """
        if len(ranges) == 1:
            leftmost, rightmost = 0, ranges[0]
        elif len(ranges) == 2:
            leftmost, rightmost = ranges
        else:
            raise ValueError(
                f"Invalid ranges `{ranges}`, number of arguments should be 1 or 2, but given {len(ranges)}."
            )
        if leftmost >= rightmost:
            raise ValueError(
                f"Invalid range, leftmost=`{leftmost}`, rightmost=`{rightmost}`."
            )
        return self._random_generator.uniform(leftmost, rightmost)
