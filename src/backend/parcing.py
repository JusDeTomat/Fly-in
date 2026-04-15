from typing import Dict, Any


def read_file(filename: str) -> Dict[str, Any]:
    """Read and parse the input file.

    Args:
        filename (str): Path to the input file.

    Returns:
        Parsed dictionary with map information.

    Raises:
        ValueError: If file cannot be read or parsed.
    """
    try:
        with open(filename, "r") as file:
            content = file.read()
            dico = parcing(content)
            test_dico(dico)
            check_link(dico)
            return dico
    except FileNotFoundError:
        raise ValueError("File not found.")
    except PermissionError:
        raise ValueError(f"The programe need permition on the {filename} file")
    except Exception as e:
        raise ValueError(e)


def parcing(content: str) -> Dict[str, Any]:
    """Parse the content of the input file into a dictionary.

    Args:
        content (str): Raw content of the file.

    Returns:
        Dictionary with parsed map data.

    Raises:
        ValueError: If parsing fails.
    """
    lst = content.split('\n')
    dico: Dict[str, Any] = {
        "nb_drones": 0,
        "start": {},
        "end": {},
        "hub": {},
        "link": []
    }
    if not len(lst):
        raise TypeError("The file is empty")
    try:
        for line in lst:
            if '#' not in line:
                if len(line.split(':')) > 1:
                    key, value = line.split(": ")
                    if key == "nb_drones":
                        if (int(value) <= 0):
                            raise TypeError("nb_drones need to be > 0 ")
                        dico["nb_drones"] = int(value)

                    if key == "start_hub":
                        if dico['start'] == {}:
                            no_parm = False
                            try:
                                mendatory, parm_add = value.split(' [')
                            except Exception:
                                no_parm = True
                                mendatory = value
                            mendatory = ' '.join(mendatory.split())
                            if len(mendatory.split(' ')) != 3:
                                raise TypeError(f"{key} need 3 parm not"
                                                f" {len(mendatory.split(' '))}"
                                                " is you want more parm do "
                                                "this [color=green ...]")
                            mendatory_splited = mendatory.split(' ')
                            name_start, x_str, y_str = mendatory_splited
                            x_start = int(x_str)
                            y_start = int(y_str)
                            dico_start: Dict[str, Any] = {
                                "name": name_start,
                                "x": x_start,
                                "y": y_start
                            }
                            dico_hub: Dict[str, Any] = {"x": x_start,
                                                        "y": y_start}
                            if not no_parm:
                                parm_add, _ = parm_add.split(']')
                                parm = parm_add.split(' ')
                                for element in parm:
                                    if element != '':
                                        parmkey, parmvalue = element.split('=')
                                        dico_start[parmkey] = parmvalue
                                        dico_hub[parmkey] = parmvalue
                            dico["start"] = dico_start
                            dico["hub"][name_start] = dico_hub
                        else:
                            raise TypeError("The programe need only"
                                            " 1 start_hub")

                    if key == "end_hub":
                        if dico['end'] == {}:
                            no_parm = False
                            try:
                                mendatory, parm_add = value.split(' [')
                            except Exception:
                                no_parm = True
                                mendatory = value
                            mendatory = ' '.join(mendatory.split())
                            if len(mendatory.split(' ')) != 3:
                                raise TypeError(f"{key} need 3 parm not "
                                                f"{len(mendatory.split(' '))}"
                                                " is you want more parm do"
                                                "this [color=green ...]")
                            mendatory_splited = mendatory.split(' ')
                            name_end, x_str, y_str = mendatory_splited
                            x_end = int(x_str)
                            y_end = int(y_str)
                            dico_end: Dict[str, Any] = {
                                "name": name_end,
                                "x": x_end,
                                "y": y_end
                            }
                            dico_hub_end: Dict[str, Any] = {"x": x_end,
                                                            "y": y_end}
                            if not no_parm:
                                parm_add, _ = parm_add.split(']')
                                parm = parm_add.split(' ')
                                for element in parm:
                                    if element != '':
                                        parmkey, parmvalue = element.split('=')
                                        dico_end[parmkey] = parmvalue
                                        dico_hub_end[parmkey] = parmvalue
                            dico["end"] = dico_end
                            dico["hub"][name_end] = dico_hub_end
                        else:
                            raise TypeError("The programe need only 1 end_hub")

                    if key == "hub":
                        no_parm = False
                        try:
                            mendatory, parm_add = value.split(' [')
                        except Exception:
                            no_parm = True
                            mendatory = value
                        mendatory = ' '.join(mendatory.split())
                        if len(mendatory.split(' ')) != 3:
                            raise TypeError(f"{key} need 3 parm not "
                                            f"{len(mendatory.split(' '))} is"
                                            " you want more parm do "
                                            "this [color=green ...]")
                        mendatory_splited = mendatory.split(' ')
                        name_hub, x_str, y_str = mendatory_splited
                        x_hub = int(x_str)
                        y_hub = int(y_str)
                        dico_hub_hub: Dict[str, Any] = {"x": x_hub, "y": y_hub}
                        if not no_parm:
                            parm_add, _ = parm_add.split(']')
                            parm = parm_add.split(' ')
                            for element in parm:
                                if element != '':
                                    parmkey, parmvalue = element.split('=')
                                    if (parmkey == "zone"
                                        and parmvalue not in [
                                            "normal",
                                            "priority",
                                            "restricted",
                                            "blocked"
                                            ]):
                                        raise TypeError(f"{parmvalue} is not a"
                                                        " good zone name")
                                    dico_hub_hub[parmkey] = parmvalue
                            if name_hub in dico['hub'].keys():
                                raise TypeError("you can't have 2 "
                                                "hub whit same name")
                        dico["hub"][name_hub] = dico_hub_hub

                    if key == "connection":
                        mendatory_conn = value.split(' [')
                        if len(mendatory_conn[0].split(' ')) != 1:
                            raise TypeError(f"{key} need 1 parm not "
                                            f"{
                                            len(mendatory_conn[0].split(' '))
                                                }"
                                            " is you want more parm do "
                                            "this [max_link_capacity=2 ...]")
                        mendatory_splited = mendatory_conn[0].split(' ')
                        name = mendatory_splited[0]
                        name_hub1, name_hub2 = name.split('-')
                        dico_link = {"hub1": name_hub1, "hub2": name_hub2}
                        if len(mendatory) == 2:
                            parm_add, _ = mendatory[1].split(']')
                            parm = parm_add.split(' ')
                            for element in parm:
                                if element != '':
                                    parmkey, parmvalue = element.split('=')
                                    dico_link[parmkey] = parmvalue
                        dico["link"].append(dico_link)
        return dico
    except TypeError as e:
        raise ValueError(e)
    except Exception:
        raise ValueError(f"This line '{line}' is not good")


def check_link(dico: Dict[str, Any]) -> None:
    """Check that all links reference existing hubs.

    Args:
        dico: Parsed dictionary.

    Raises:
        ValueError: If a link references a non-existent hub.
    """
    try:
        p = 0
        link = dico["link"]
        for element in link:
            dico["hub"][element['hub1']]
            p = 1
            dico["hub"][element['hub2']]
    except Exception:
        if not p:
            raise ValueError(f"The connection ({element}) can't exist because"
                             f" {element['hub1']} does not exist")
        else:
            raise ValueError(f"The connection ({element}) can't exist because"
                             f" {element['hub2']} does not exist")


def test_dico(dico: Dict[str, Any]) -> None:
    """Validate the parsed dictionary for required elements.

    Args:
        dico: Parsed dictionary.

    Raises:
        ValueError: If required elements are missing or invalid.
    """
    if dico['start'] == {}:
        raise ValueError('The progrqme need start_hub')
    if dico['end'] == {}:
        raise ValueError('The progrqme need end_hub')
    if int(dico['start'].get('max_drones',
                             dico['nb_drones'])) < dico['nb_drones']:
        raise ValueError('Start max_drone need to be bigger or egal')
    if int(dico['end'].get('max_drones',
                           dico['nb_drones'])) < dico['nb_drones']:
        raise ValueError('End max_drone need to be bigger or egal')
