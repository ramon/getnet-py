import re

import setuptools

# Get the version
version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open("getnet/__init__.py", "r") as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        VERSION = match.group(1)
    else:
        raise RuntimeError("No version number found!")

APP_NAME = "getnet-py"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=APP_NAME,
    version=VERSION,
    description="A Getnet Santander SDK",
    long_description=long_description,
    author="Ramon Soares",
    author_email="contato@ramonsoares.com",
    url="https://github.com/ramon/getnet-py",
    packages=setuptools.find_packages(),
    python_requires=">=3.2",
    install_requires=["requests>=2.0.0", "requests-oauthlib>=1.2.0"],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    tests_require=["mock", "requests-mock"],
    test_suite="tests",
)
