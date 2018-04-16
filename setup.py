from setuptools import setup

setup(
    name='csvtools',
    version='0.1',
    py_modules=['csvformula', 'csvgroup', 'header', 'column_functions'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        csvformula=csvformula:csvformula
        csvgroup=csvgroup:csvgroup
    ''',
)
