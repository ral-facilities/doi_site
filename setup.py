import os

from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="doi_site",
    version="1.1.0",
    packages=["doi_site", "mds", "datasets"],
    include_package_data=True,
    license="BSD License",
    description="A simple Django app to wrap datacite calls.",
    long_description=README,
    url="http://stfc.ac.uk/",
    author="Antony Wilson",
    author_email="antony.wilson@stfc.ac.uk",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    # Adds dependencies
    install_requires=[
        "Django==3.2",
        "django-auth-ldap",
        "python-ldap",
        #"psycopg2-binary",
        "requests"
    ],
)
