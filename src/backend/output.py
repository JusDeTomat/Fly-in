from typing import List, Any


def write_output(filename: str, lst_output: List[List[Any]]) -> None:
    """Write the output to the specified file.

    Args:
        filename (str): Name of the output file.
        lst_output: List of output lists for each ship.

    Raises:
        ValueError: If file cannot be written or checked.
    """
    try:
        check_filename(filename)
        with open(filename, "w") as file:
            for i in range(len(lst_output[0])):
                for line in lst_output:
                    if line[i] is not None:
                        file.write(f"{line[i]} ")
                file.write("\n")
    except Exception as e:
        raise ValueError(e)


def check_filename(filename: str) -> None:
    """Check if the filename is valid for writing.

    Args:
        filename (str): Filename to check.

    Raises:
        ValueError: If filename is invalid or file cannot be accessed.
    """
    filesplited = filename.split('.')
    if filesplited[-1] != "txt":
        raise ValueError("You can write only in txt files")
    try:
        with open(filename, "w") as _:
            pass
    except FileNotFoundError:
        raise ValueError("File not found.")
    except PermissionError:
        raise ValueError(f"The programe need permition on the {filename} file")
    except Exception as e:
        raise ValueError(e)
