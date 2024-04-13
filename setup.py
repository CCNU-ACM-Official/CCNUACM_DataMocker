from setuptools import setup

setup(
    name="ccnuacm_datamocker",
    version="0.0.1",
    description="A data mocking library for CCNU ACM",
    author="JixiangXiong",
    author_email="xiongjx751@qq.com",
    url="https://github.com/CCNU-ACM-Official/CCNUACM_DataMocker.git",
    packages=["ccnuacm_datamocker"],
    install_requires=[
        "numpy",
        "jupyter",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Unstable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    long_description=open("README.md", "r").read(),
)
