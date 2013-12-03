# encoding: utf-8

from distutils.core import setup

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''

setup(name='audiocalc',
      version='0.0.4',
      description='A few audio/sound calculation utilities',
      long_description=description,
      author='Marian Steinbach',
      author_email='marian@sendung.de',
      url='https://github.com/marians/audiocalc',
      packages=['audiocalc'],
      license='MIT',
      requires=[])
