import os
from setuptools import setup, find_packages

# Read requirements.txt line by line and ignore comments/empty lines
with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), "r") as f:
    requirements = [
        line.strip() for line in f.readlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="playwright_pytest_project",
    version="0.0.1",
    author="Roman Horowitz",
    description="Basic Test Framework",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)
