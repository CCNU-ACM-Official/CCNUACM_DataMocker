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

Here is a basic example of how to use the data mocker:

```python
from ccnuacm_datamocker.data_model import *
import ccnuacm_datamocker as dm

dm.set_seed(751)
dm.set_work_dir(".")
dm.set_compiler("D:/mingw/bin/g++.exe")

ds = DataSet(name="P751", std_path="./std/P751.cpp")

ds.add(Sequence(LowercaseCharSet() + DigitCharSet(), length=10, sep=''))
ds.add(Sequence(BinaryCharSet(), length=10, sep=' '))

ds.run()
```

## Contributing

Contributions are welcome. Please submit a pull request or create an issue to discuss the changes you want to make.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions, please feel free to post an issue.

