import os

import click
import sympy as sp

from transfer_function_calculator.assets.netlist import COMMON_EMITTER
from transfer_function_calculator.calc import calculate_transfer_function


@click.command()
@click.option("-s", "--spice", "file_type", flag_value="spice", help="Process a SPICE file.")
@click.option("-t", "--text", "file_type", flag_value="text", help="Process a text file.")
@click.argument("file_path", type=click.Path(exists=True))
def tf_calc(file_type, file_path):
    """CLI tool to parse a file and pass it to the calc module."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        # Read and process the file content
        with open(file_path, "r") as file:
            content = file.read()

        if file_type == "spice" or file_type == "text":
            formatted_content = format_content(content)
        else:
            raise click.BadParameter("You must specify either --spice or --text.")
        print(formatted_content)
        # Pass the processed content to calc.py
        tf = calculate_transfer_function(COMMON_EMITTER)

        # Log the output within a decorative ASCII box
        print_asc_box(tf)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


def format_content(content):
    """Format the content of a SPICE file to a Python string."""
    # Implement the logic to parse and format SPICE content
    formatted_content = f"\n{content}"
    return formatted_content


def print_asc_box(tf):
    """Utility function to print text within an ASCII box."""
    print("\nNormalized Transfer Function H(s):")
    sp.pprint(tf, use_unicode=True)


if __name__ == "__main__":
    tf_calc()
