import os
import subprocess

import click
import sympy as sp

from transfer_function_calculator.calculator import calculate_transfer_function


@click.command()
@click.option("-t", "--text", "file_type", flag_value="text", help="Process a text file.")
@click.option("-j", "--jupyter", "start_jupyter", is_flag=True, help="Start a Jupyter Notebook.")
@click.argument("file_path", type=click.Path(exists=True), required=False)
def tf_calc(file_type, file_path, start_jupyter):
    try:
        if start_jupyter:
            notebook_path = "./transfer_function_calculator/notebooks/main.ipynb"
            subprocess.Popen(
                [
                    "jupyter",
                    "notebook",
                    notebook_path,
                    "--NotebookApp.token=''",
                    "--NotebookApp.password=''",
                ]
            )
            return

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        with open(file_path, "r") as file:
            content = file.read()

        if file_type in ["text"]:
            formatted_content = format_content(content)
        else:
            raise click.BadParameter("You must specify either -t or -j.")

        tf, _ = calculate_transfer_function(formatted_content)
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
