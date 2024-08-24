import os

import click
import sympy as sp

from transfer_function_calculator.calculator import calculate_transfer_function


@click.command()
@click.option("-s", "--spice", "file_type", flag_value="spice", help="Process a SPICE file.")
@click.option("-t", "--text", "file_type", flag_value="text", help="Process a text file.")
@click.option("-n", "--net", "file_type", flag_value="net", help="Process a net file.")
@click.argument("file_path", type=click.Path(exists=True))
def tf_calc(file_type, file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        with open(file_path, "r") as file:
            content = file.read()

        if file_type in ["spice", "text", "net"]:
            formatted_content = format_content(content)
        else:
            raise click.BadParameter("You must specify either --spice, --net or --text.")

        tf = calculate_transfer_function(formatted_content)
        print("\nNormalized Transfer Function H(s):")
        sp.pprint(tf, use_unicode=True)
        print("\n")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


def format_content(content):
    formatted_content = f"{content}"
    return formatted_content


if __name__ == "__main__":
    tf_calc()
