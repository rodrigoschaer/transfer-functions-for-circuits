# Circuit Transfer Function Calculator

This project is an application for calculating transfer functions of small signal model of transistors.

# Usage

To run the application, follow these steps:

1. Install the required dependencies using `pip install -r requirements.txt`.
2. Run main application with `python3 main.py`

# Current and next steps

At first a got a little bit ahead of myself and underestimated the complexity for the app's core main task, now I'm starting fresh from the basics:

- [x] Get a transfer function small signal model amplifier circuit

Next steps:

- [x] Find a way of putting the answer in a polynomial format;
- [x] Create a way of passing the analyzed circuit via spice file;
- [x] Make it as a CLI tool
- [x] Make it to work as a python notebook
- [ ] Maybe make a LTSpice plugin (this one is really long term)

# How to Setup this project

Run the following commands:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You can run locally or build the library:

```bash
python transfer_function_calculator/main.py -t ./transfer_function_calculator/samples/rlc.txt
```

Build:

```bash
python setup.py sdist bdist_wheel & pip install -e .
```

And run:

```bash
tf-calc -t ./transfer_function_calculator/samples/rlc.txt
```

Clean up build files and run again:

```bash
rm -rf build dist transfer_function_calculator.egg-info & python setup.py sdist bdist_wheel & pip install -e .
```

## Run Modes

1. File mode, prints in terminal:

```bash
tf-calc -t ./transfer_function_calculator/samples/rlc.txt
```

2. Jupyter mode, opens interface in browser:

```bash
tf-calc -j
```

## License

This project is licensed under the MIT License.
