import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nnv",
    version="0.0.5",
    author="Renato Cordeiro",
    author_email="opensource@renatocordeiro.com",
    description="A simple and easy to use tool to visualize Neural Networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renatosc/nnv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)