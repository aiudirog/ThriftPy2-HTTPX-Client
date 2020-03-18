import versioneer
from setuptools import setup

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=[
        "thriftpy2>=0.4.11",
        "httpx",
        "typing_extensions; python_version < '3.8'",
    ],
)
