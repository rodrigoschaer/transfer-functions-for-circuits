from setuptools import find_packages, setup

setup(
    name="transfer-function-calculator",
    version="0.1.0",
    description="A CLI tool to calculate transfer functions from SPICE or text files.",
    author="Rodrigo Ferreira Schaer",
    author_email="rodrigo.fscs@gmail.com",
    url="https://github.com/rodrigoschaer/transfer-function-calculator",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "sympy",
    ],
    entry_points={
        "console_scripts": [
            "tf-calc=transfer_function_calculator.main:tf_calc",  # Update path to main.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
