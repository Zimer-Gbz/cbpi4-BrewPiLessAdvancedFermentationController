from setuptools import setup
from os import path

# Lê o conteúdo do README.md para usar como descrição longa
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cbpi4-BrewPiLessAdvancedFermentationController',
    version='0.1',
    description='Plugin de controle avançado de fermentação para CraftBeerPi 4 inspirado no BrewPiLess',
    author='Gustavo Zimer',
    author_email='',  # opcional
    url='https://github.com/Zimer-Gbz/cbpi4-BrewPiLessAdvancedFermentationController',
    include_package_data=True,
    package_data={
        # Inclui arquivos extras como config.yaml
        '': ['*.txt', '*.rst', '*.yaml', '*.json'],
        'cbpi4-BrewPiLessAdvancedFermentationController': [
            '*', '*.txt', '*.rst', '*.yaml', '*.json'
        ]
    },
    packages=['cbpi4-BrewPiLessAdvancedFermentationController'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
