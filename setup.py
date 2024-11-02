# This is a very old way of configuring python packages.
# Modern python codebases use a proper dependency manager like poetry.
from setuptools import setup, find_packages

# Read requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="math_quiz",
    version="0.1",
    packages=find_packages(),
    install_requires=required,
    author="Zurab Mujirishvili",
    author_email="zurab.mujirishvili@fau.de",
    description="A simple math quiz game",
    keywords="math, quiz, game",
    url="https://github.com/zuka011/DSSS-Homework-2",
        entry_points={
        'console_scripts': [
            'math_quiz=math_quiz.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
