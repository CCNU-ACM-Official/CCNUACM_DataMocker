from setuptools import setup

# 读取 requirements.txt 文件中的依赖项
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ccnuacm_datamocker",
    version="0.0.1",
    description="A data mocking library for CCNU ACM",
    author="JixiangXiong",
    author_email="xiongjx751@qq.com",
    url="https://github.com/CCNU-ACM-Official/CCNUACM_DataMocker.git",
    packages=["ccnuacm_datamocker"],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Unstable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
