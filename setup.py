from setuptools import setup, find_packages

setup(
    name="cbpi4-BrewPiLessAdvancedFermentationController",   # mesmo nome do plugin.json
    version="0.1",
    author="Gustavo Zimer",
    description="Plugin de controle avançado de fermentação para CraftBeerPi 4 inspirado no BrewPiLess",
    packages=find_packages(),  # vai pegar os pacotes Python na pasta
    include_package_data=True,  # inclui arquivos externos (ex: config.yaml)
    install_requires=[
        # Coloque aqui alguma dependência que seu plugin precise, exemplo:
        # 'numpy',
    ],
    entry_points={
        "cbpi4.fermenter_controller": [
            "BrewPiLessAdvancedFermentationController = brewpiless_fermentation:BrewPiLessAdvancedFermentationController",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',
)

