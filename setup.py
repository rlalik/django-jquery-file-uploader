"""
django-jquery-file-uploader
"""
import sys

from setuptools import setup
from setuptools.command.test import test

def run_tests(*args):
    from jqfuploader.tests import run_tests
    errors = run_tests()
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


test.run_tests = run_tests

setup(
    name="django-jquery-file-uploader",
    version="0.0.1",
    packages=['jqfuploader'],
    license="The MIT License (MIT)",
    include_package_data = True,
    description=("A Django backend for jQuery File Upload."),
    long_description=("A django project, greatly based and inspired by "
                "https://github.com/tcztzy/django-multiple-file-chunked-upload "
                "containing an app for BasicPlusUI jquery file upload form "
                "based on the work by Sebastian Tschan: "
                "https://github.com/blueimp/jQuery-File-Upload"),
    author="Rafal Lalik",
    author_email="rafallalik@gmail.com",
    maintainer="Rafal Lalik",
    maintainer_email="rafallalik@gmail.com",
    url="https://github.com/rlalik/django-jquery-file-uploader/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    test_suite="dummy",
)
