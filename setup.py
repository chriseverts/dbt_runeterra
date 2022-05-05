from setuptools import find_packages, setup

setup(
    install_requires=[
        "gitdb2==2.0.6",
        "gitpython==3.0.5",
        "numpy==1.18.1",
        "pandas==1.0.0",
        "pathlib==1.0.1",
        "python-dateutil==2.8.1",
        "pytz==2019.3",
        "six==1.14.0",
        "smmap2==2.0.5",
    ],
    name="src",
    packages=find_packages(),
    description="A personal tracker for Legends of Runeterra games.",
    author="Guillaume Legoy",
)
