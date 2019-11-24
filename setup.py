import re
import sys
from pathlib import Path
from setuptools import setup

ROOT = Path(__file__).parent

if sys.version_info < (3, 5):
    raise SystemExit('This requires Python 3.5+')

with open(str(ROOT / 'src' / 'engine' / 'meta.py'), encoding='utf-8') as f:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open(str(ROOT / 'README.md'), encoding='utf-8') as f:
    README = f.read()

with open(str(ROOT / 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()


setup(
    name='flutter_engine',
    author='Valentin B.',
    author_email='valentin.be@protonmail.com',
    url='https://github.com/flutter-py/engine',
    license='Apache-2.0/MIT',
    description='Python bindings to the Flutter engine',
    long_description=README,
    project_urls={
        'Source': 'https://github.com/flutter-py/engine',
        'Issue tracker': 'https://github.com/flutter-py/engine/issues'
    },
    version=VERSION,
    package_dir={'': 'src', 'flutter_engine': 'src/engine'},
    packages=['flutter_engine'],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    python_requires='>=3.5.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Multimedia',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: User Interfaces',
    ],
)
