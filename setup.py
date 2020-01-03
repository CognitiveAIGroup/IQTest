from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('iqtest/version.py')

with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)
setup(
    name="iqtestsdk",
    version=main_ns['__version__'],
    keywords=["class", "boilerplate"],
    description="iqtest sdk",
    long_description="iqtest sdk for run your model locally",
    license="MIT Licence",

    url="https://iqtest.pub",
    author="Wang Haibo",
    author_email="hbwang@bsbii.cn",

    packages=find_packages(),
    platforms="any",
    install_requires=[],

    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
