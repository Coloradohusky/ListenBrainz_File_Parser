from os import path
from typing import List

from setuptools import setup, find_packages

from listenbrainz_file_parser.main import get_version


def read_multiline_as_list(file_path: str) -> List[str]:
    with open(file_path) as file_handler:
        contents = file_handler.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


with open('README.md', 'r') as f:
    long_description = f.read()

requirements = read_multiline_as_list("requirements.txt")

setup(
    name='listenbrainz_file_parser',
    version=get_version(),
    description='Parses lists of listened music and uploads to ListenBrainz.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Coloradohusky/ListenBrainz_File_Parser/',
    author='Coloradohusky',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'listenbrainz_file_parser = listenbrainz_file_parser.main:main',
        ],
    },
    python_requires='>=3.5, <4',
    install_requires=requirements,
)