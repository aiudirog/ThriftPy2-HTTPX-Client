import versioneer
from setuptools import setup

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=[
        'thriftpy2>=0.4.10',
        'httpx',
    ],
)
