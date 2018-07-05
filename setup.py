from setuptools import find_packages
from setuptools import setup

with open("requirements.txt", "r") as f:
    install_requires = [line.strip() for line in f.readlines()]

with open("requirements-dev.txt", "r") as f:
    dev_requires = [line.strip() for line in f.readlines()]


setup(
    name="",
    version='0.0.1',
    description='Simple Merkle Tree',
    long_description="",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU v3 License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    url='https://github.com/forever-am/fcredis',
    author='Alice Wang',
    author_email="alice.wang@forever-am.com",
    keywords='merkle tree, blockchain',
    license="GNU v3",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"test": dev_requires}
)
