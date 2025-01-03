"""Setup script."""
from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="veggie",
    version="0.1.11",
    author="Theodore Tsitsimis",
    author_email="th.tsitsimis@gmail.com",
    description="A tool to monitor and execute Celery tasks",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "dash>=2.5.1",
        "dash-extensions>=1.0.19",
        "dash-mantine-components>=0.15.1",
        "dash-iconify",
        "loguru",
        "celery[redis]",
        "humanize",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
)
