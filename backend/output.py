def write_output(filename, lst_output):
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


def check_filename(filename):
    filesplited = filename.split('.')
    if filesplited[-1] == "py":
        raise ValueError("You can't write in python files")
    try:
        with open(filename, "w") as _:
            pass
    except FileNotFoundError:
        raise ValueError("File not found.")
    except PermissionError:
        raise ValueError(f"The programe need permition on the {filename} file")
    except Exception as e:
        raise ValueError(e)
