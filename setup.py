"""Setup script for the glucose reading tool."""
from setuptools import setup, find_packages

requirements = [
    "sqlalchemy~=1.4.32,<2.0",
    "pydantic~=1.9.0",
    "fastapi~=0.75.0",
    "uvicorn~=0.17.6"
]

extra_requirements = {
    "dev": [
        "black==22.1.0",
        "coverage==6.3.2",
        "mypy==0.941",
        "mypy-extensions==0.4.3",
        "pylint==2.12.2",
        "pytest==7.1.1",
        "sqlalchemy2-stubs==0.0.2a20",
    ]
}

setup(
    name="glucose-reading-store",
    version="0.0.1",
    author="Travis Hesketh",
    author_email="travis@hesketh.scot",
    description="CRUD application to track glucose readings for diabetic patients.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require=extra_requirements,
    entry_points={
        'console_scripts': ['glucose-reading-server=glucose_reading_server.__main__:main']
    }
)
