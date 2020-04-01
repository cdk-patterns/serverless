import setuptools


setuptools.setup(
    name="the_lambda_lith",
    version="0.0.1",

    description="The Lambda-lith",
    long_description="A flask app inside a lambda",
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "flask"},
    packages=setuptools.find_packages(where="flask"),

    install_requires=[
        "aws-wsgi==0.2.6",
        "Flask==1.1.1"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)