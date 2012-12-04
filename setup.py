from distutils.core import setup

setup(
        name='python-moab',
        version='0.2',
        author='Michael Gutteridge',
        author_email='mrg@fhcrc.org',
        packages=['mwm', ],
        url='',
        license='LICENSE.txt',
        description='Modules for interfacing with MWM.',
        long_description=open('README.txt').read(),
        install_requires=[
            "ElementTree >= 1.3.0",
        ],
)
