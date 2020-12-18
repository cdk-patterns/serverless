import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="the_media_live_stream",
    version="0.0.1",

    description="The media live stream CDK example",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Leandro Damascena (https://github.com/Cloud-Architects)",

    package_dir={"": "the_media_live_stream"},
    packages=setuptools.find_packages(where="the_media_live_stream"),

    install_requires=[
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
