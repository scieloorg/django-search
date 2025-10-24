from setuptools import setup, find_packages

setup(
    name='scielo-search',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "wagtail>=6.0",
    ],
    author="SciELO",
    description="Página de busca personalizável para Wagtail",
    url="https://github.com/scieloorg/scielo-search",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Wagtail",
    ],
)