import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyTransportNSW",
    version="0.0.6",
    author="Dav0815",
    description="Get transport information from TransportNSW",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dav0815/TransportNSW",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
