try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Toy Graph DB using Key Value store',
    'author': 'Anuj Khare',
    'url': 'https://github.com/anujkhare/graphKV',
    'download_url': 'https://codeload.github.com/anujkhare/graphKV/zip/master',
    'author_email': 'khareanuj18@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'graphKV'
}

setup(**config)
