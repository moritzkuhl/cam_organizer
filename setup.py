from setuptools import setup

setup(
    name='cameraroll_organizer',
    version='1.0',
    py_modules=['cameraroll_organizer'],
    install_requires=['click','pillow','exifread<3','PyExifTool'],
    entry_points='''
        [console_scripts]
        cameraroll_organizer=cameraroll_organizer:cli
    ''',
)