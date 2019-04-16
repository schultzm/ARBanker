from setuptools import setup
import arbanker
import os

def read(fname):
    '''
    Read the README
    '''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'arbanker',
    version = ARBanker.__version__,
    description = ARBanker.__description__,
    long_description=read('README.md'),
    classifiers = ['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: GNU Affero General ' +
                   'Public License v3 or later (AGPLv3+)',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Scientific/Engineering :: Medical Science Apps.',
                   'Intended Audience :: Science/Research'],
    keywords = ['pipeline',
                'ruffus',
                'bacteria',
                'contigs',
                'assembly',
                'assemblies',
                'reads',
                'paired-end',
                'public health microbiology',
                'microbial genomics'],
    download_url = ARBanker.__download_url__,
    author = ARBanker.__author__,
    author_email = ARBanker.__author_email__,
    license = ARBanker.__license__,
    packages = ['ARBanker'],
    scripts = ['ARBanker/arbanker'],
    include_package_data = True,
    install_requires = []
    )