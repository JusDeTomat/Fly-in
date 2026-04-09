import visual.visual as vis
import backend.dijkstrar as dij
import backend.parcing as par
import backend.output as out

def fly_in():
	try:
		dico = par.read_file("input.txt")
		maps = dij.Map(dico)
		solve = maps.solve()
		out.write_output("outputt.py.txt", maps.lst_output)
		vis.main_visual(dico, solve)
	except ValueError as e:
		print(f"[ERROR]: {e}")

if(__name__ == "__main__"):
	fly_in()