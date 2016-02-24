from setuptools import setup, find_packages

setup(
    name="django-charity-check",
    version="1.0",
    author="Andrew Young",
    author_email="ayoung@thewulf.org",
    description="A utility plugin for verifying non-profits IRS status.",
    packages=find_packages(exclude=["tests"])
    )
