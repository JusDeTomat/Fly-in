def read_file(filename: str):
    try:
        with open(filename, "r") as file:
            content = file.read()
            dico = parcing(content)
            check_link(dico)
            return dico
    except FileNotFoundError:
        raise ValueError("File not found.")
    except PermissionError:
        raise ValueError(f"The programe need permition on the {filename} file")
    except Exception as e:
        raise ValueError(e)

def parcing(content):
    lst = content.split('\n')
    dico = {
        "nb_drones" : 0,
        "start": [],
        "end" : [],
        "hub" : {},
        "link" : []
    }
    if len(lst) and "nb_drones:" not in lst[0]:
        raise TypeError("The very firth line on the file need to be 'nb_drones: (int)'")
    try:
        for line in lst:
            if len(line.split(':')) > 1:
                key, value = line.split(": ")
                if key == "nb_drones":
                    dico["nb_drones"] = int(value)
                
                if key == "start_hub":
                    mendatory, parm_add = value.split(' [')
                    if len(mendatory.split(' ')) != 3:
                        raise TypeError(f"{key} need 3 parm not {len(mendatory.split(' '))} is you want more parm do this [color=green ...]")
                    mendatory_splited = mendatory.split(' ')
                    name, x, y = mendatory_splited
                    dico_start = {"name": name, "x": x, "y": y}
                    dico_hub = {"x": x, "y": y}
                    parm_add, _ = parm_add.split(']')
                    parm = parm_add.split(' ')
                    for element in parm:
                        if element != '':
                            parmkey, parmvalue = element.split('=')
                            dico_start[parmkey] = parmvalue
                    dico["start"] = dico_start
                    dico["hub"][name] = dico_hub
                
                if key == "end_hub":
                    mendatory, parm_add = value.split(' [')
                    if len(mendatory.split(' ')) != 3:
                        raise TypeError(f"{key} need 3 parm not {len(mendatory.split(' ')) - 2} is you want more parm do this [color=green ...]")
                    mendatory_splited = mendatory.split(' ')
                    name, x, y = mendatory_splited
                    dico_end = {"name": name, "x": x, "y": y}
                    dico_hub = {"x": x, "y": y}
                    parm_add, _ = parm_add.split(']')
                    parm = parm_add.split(' ')
                    for element in parm:
                        if element != '':
                            parmkey, parmvalue = element.split('=')
                            dico_end[parmkey] = parmvalue
                    dico["end"] = dico_end
                    dico["hub"][name] = dico_hub
                
                if key == "hub":
                    mendatory, parm_add = value.split(' [')
                    if len(mendatory.split(' ')) != 3:
                        raise TypeError(f"{key} need 3 parm not {len(mendatory.split(' '))} is you want more parm do this [color=green ...]")
                    mendatory_splited = mendatory.split(' ')
                    name, x, y = mendatory_splited
                    dico_hub = {"x": x, "y": y}
                    parm_add, _ = parm_add.split(']')
                    parm = parm_add.split(' ')
                    for element in parm:
                        if element != '':
                            parmkey, parmvalue = element.split('=')
                            dico_hub[parmkey] = parmvalue
                    dico["hub"][name] = dico_hub
                
                if key == "connection":
                    mendatory= value.split(' [')
                    if len(mendatory[0].split(' ')) != 1:
                        raise TypeError(f"{key} need 1 parm not {len(mendatory[0].split(' '))} is you want more parm do this [max_link_capacity=2 ...]")
                    mendatory_splited = mendatory[0].split(' ')
                    name = mendatory_splited
                    name_hub1, name_hub2 = name[0].split('-')
                    dico_link = {"hub1": name_hub1, "hub2": name_hub2}
                    if len(mendatory)  == 2:
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
    except Exception as e:
        raise ValueError(f"This line '{line}' is not good\n"
                         f"[DEV] : {e}")
    
def check_link(dico):
    try:
        p = 0
        link = dico["link"]
        for element in link:
            dico["hub"][element['hub1']]
            p = 1
            dico["hub"][element['hub2']]
    except Exception:
        if not p:
            raise ValueError(f"The connection ({element}) can't exist because {element['hub1']} does not exist")
        else:
            raise ValueError(f"The connection ({element}) can't exist because {element['hub2']} does not exist")






def main():
    try:
        print(read_file("test.txt"))
    except ValueError as e:
        print(f"[ERROR] : {e}")
    
if __name__ == "__main__":
    main()