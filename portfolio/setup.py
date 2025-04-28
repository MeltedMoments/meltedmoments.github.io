from setuptools import setup, find_packages

setup(
    name='portfolio',                  # package name
    version='0.1.3',                   # version number
    packages=find_packages(where=".", include=["portfolio", "projects/*"]),
    package_dir={"": "."},
    install_requires=[
        # List any 3rd party packages you need, e.g.
        # "pandas>=2.0",
    ],
    python_requires='>=3.9',          
    include_package_data=True,
    description='Reusable code for annotation and Label Studio projects',
    author='Jennie Yip',
)
