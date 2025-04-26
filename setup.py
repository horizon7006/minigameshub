# setup.py
from setuptools import setup, find_packages

setup(
  name="MiniGamesHub",
  version="1.0.0",
  packages=find_packages(),
  include_package_data=True,
  install_requires=["pygame>=2.1.0"],
  entry_points={
    "console_scripts": [
      "minigameshub = main:main",  # if you wrap your run in a main() fn
    ]
  }
)
