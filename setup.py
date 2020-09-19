import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hashtag-generator", # Replace with your own username
    version="0.0.1",
    author="Get Ahead Tutpr",
    author_email="info.getaheadtutoring@gmail.com",
    description="A hashtag generator for instagram.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ace-it-dev-interns/hashtag-generator/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
