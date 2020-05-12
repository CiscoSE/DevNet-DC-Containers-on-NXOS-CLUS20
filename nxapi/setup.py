import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nxapi",
    version="0.1.0",
    author="Timothy E. Miller, PhD",
    author_email="timmil@cisco.com",
    description="Python interface to handle Cisco Nexus NX-API communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gve-vse-tim/nexus9000_nxapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7', 
    install_requires=[
        'flake8~=3.7.9',
        'requests~=2.23.0',
        'prometheus-client~=0.7.1'
    ]
)
