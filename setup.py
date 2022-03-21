"""Setup script for the glucose reading tool."""
from setuptools import setup, find_packages

setup(
    name="sensyne-glucose-readings",
    version="0.0.1",
    author="Travis Hesketh",
    author_email="travis@hesketh.scot",
    description="Tech test submission for Sensyne.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
)
