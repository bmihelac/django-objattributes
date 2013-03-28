from setuptools import setup, find_packages


VERSION = __import__("objattributes").__version__

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]

install_requires = [
    'Django>=1.4.2',
]

setup(
    name="django-objattributes",
    description="Django objattributes",
    version=VERSION,
    author="Informatika Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://github.com/bmihelac/django-objattributes",
    packages=find_packages(exclude=["tests"]),
    package_data={},
    include_package_data=True,
    install_requires=install_requires,
)
