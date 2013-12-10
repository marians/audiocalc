# encoding: utf-8

from os.path import join

try:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup
except:
    from distutils.core import setup

from distutils.extension import Extension
from Cython.Distutils import build_ext

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''

PKG_DIR = 'audiocalc'

extensions = [
    Extension(
        PKG_DIR + "._audiocalc",
        sources=[join(PKG_DIR, "_audiocalc.pyx")],
    )
]

setup(name='audiocalc',
    version='0.0.9',
    description='A few audio/sound calculation utilities',
    long_description=description,
    author='Marian Steinbach',
    author_email='marian@sendung.de',
    url='https://github.com/marians/audiocalc',
    packages=['audiocalc'],
    license='MIT',
    requires=[],
    ext_modules = extensions,
    cmdclass = {'build_ext': build_ext}
)