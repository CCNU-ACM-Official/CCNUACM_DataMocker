# CCNUACM DataMocker

## Description

This project is a data mocker for CCNUACM. It is written in Python. Source code is available
on our [Github repo:CCNUACM_DataMocker](https://github.com/CCNU-ACM-Official/CCNUACM_DataMocker.git).

## Installation

To install the necessary dependencies, run the following command:

```bash
pip3 install ccnuacm-datamocker -U
```

## Usage

Following is a basic example of how to use the data mocker. More examples are avaliable [here](https://github.com/CCNU-ACM-Official/CCNUACM_DataMocker/tree/master/examples).

```python
import ccnuacm_datamocker as dm
from ccnuacm_datamocker.data_model import *
import os

dm.set_seed(0)
dm.set_work_dir(".")
dm.set_compiler("D:/mingw/bin/g++.exe")

os.makedirs("./std", exist_ok=True)

open("./std/APlusB.cpp", "w").write(
    """
#include <iostream>

int32_t main() {
  int64_t T;
  std::cin >> T;
  while (T--) {
    int64_t a, b;
    std::cin >> a >> b;
    std::cout << a + b << '\\n';
  }
  return 0;
}
"""
)

ds = DataSet(name="APlusB", std_path="./std/APlusB.cpp")

ds.add(
    RandomInt(low=1, high=100)
    .repeat(times=2, sep=" ")
    .repeat(times=10, sep="\n", show_times=True, h_sep="\n"),
    reputation=2,
)

ds.show()

ds.run()
```



## Contributing

Contributions are welcome. Please submit a pull request or create an issue to discuss the changes you want to make.

## License

This project is licensed under the [MIT License](https://github.com/CCNU-ACM-Official/CCNUACM_DataMocker/blob/master/LICENSE).

## Contact

If you have any questions, please feel free to post an issue.

