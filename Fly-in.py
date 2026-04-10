import sys
import src.visual.visual as vis
import src.backend.dijkstrar as dij
import src.backend.parcing as par
import src.backend.output as out


def fly_in():
    if len(sys.argv) != 3:
        print("[ERROR]: you need to use 'python3 Fly-in.py "
              "input.txt output.txt")
        sys.exit(1)
    try:
        dico = par.read_file(sys.argv[1])
        maps = dij.Map(dico)
        solve = maps.solve()
        out.write_output(sys.argv[2], maps.lst_output)
        vis.main_visual(dico, solve)
    except ValueError as e:
        print(f"[ERROR]: {e}")


if (__name__ == "__main__"):
    fly_in()
