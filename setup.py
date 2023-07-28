from setuptools import setup


setup(
    name = "ycf",
    version = "0.0.1",
    author="UMadd",
    description = "Script that helps solving problems",
    packages = ["ycf"],
    entry_points={
        "console_scripts": [
            "ycf = ycf.main:main",
            ]
        },
    )


