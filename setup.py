from setuptools import setup, find_packages

setup(
    name="pygame-wrapper",
    version="0.1.2",
    description="A lightweight Pygame wrapper that simplifies game development",
    author="Talha Orak",
    author_email="talhaorak@users.noreply.github.com",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
