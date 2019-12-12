from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    url="https://github.com/rajeshwar-sopho/flask-tutorial",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)