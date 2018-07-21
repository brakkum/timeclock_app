from setuptools import setup


def read(file):
    with open(file, 'r') as rm:
        return rm.read()

setup(  
    name='time_clock',
    version='0.1',
    description='For keeping track of time spent on projects',
    long_description=read('README.rst'),
    url='http://github.com/brakkum/timeclock_app',
    author='Daniel Brakke',
    author_email='brakphoto@gmail.com',
    keywords='timeclock time management',
    license='MIT',
    packages=['time_clock'],
    install_requires=[
    ],
    entry_points= {
        'console_scripts': [
            'time_clock = time_clock.__main__:main'
        ]
    },
    include_package_data=True)