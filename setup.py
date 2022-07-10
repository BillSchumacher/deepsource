from os.path import exists

from setuptools import find_packages, setup

setup(
    name="deepsource",
    author="Bill Schumacher",
    author_email="william.schumacher@gmail.com",
    packages=find_packages(),
    scripts=[],
    url="https://github.com/BillSchumacher/deepsource",
    license="MIT",
    description="A python scanner, work in progress...",
    long_description=open("README.rst").read() if exists("README.rst") else "",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
    ],
    install_requires=["celery", "redis"],
    version="0.1.1",
    zip_safe=False,
)
