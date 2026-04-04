class Hub:
    def __init__(self, name, x, y, zone, max_drone):
        self.lst_link = []
        self.name = name
        self.visited = False
        self.x = x
        self.y = y
        self.zone = zone
        self.nb_in = 0
        self.max_in = max_drone
        self.cost = 0

class Map:
    def __init__(self, dico_info):
        self.dico = dico_info
        self.lst_hub = []
        self.add_all_hub()
        self.start_name = dico_info['start']['name']
        self.end_name = dico_info['end']['name']
        self.finish_solve = False
        self.lst_solve = []
        self.lst_cost = []
        self.lst_choose = []

    def add_all_hub(self):
        key_hub = self.dico["hub"].keys()
        link = self.dico["link"]
        for name_hub in key_hub:
            hub = Hub(
                name_hub,
                self.dico['hub'][name_hub]['x'],
                self.dico['hub'][name_hub]['y'],
                self.dico['hub'][name_hub].get('zone', 'normal'),
                self.dico['hub'][name_hub].get('max_drones', 1)

            )
            self.lst_hub.append(hub)
        for hub in self.lst_hub:
            for element in link:
                if element['hub1'] == hub.name:
                    for hub2 in self.lst_hub:
                        if hub2.name == element['hub2']:
                            hub.lst_link.append(hub2)
            
    
    def solve(self):
        self.finish_solve = False
        for hub in self.lst_hub:
            if hub.name == self.start_name:
                hub_start = hub
        self.dijkstrar(hub_start,0)
        hub_solve = self.lst_choose[-1][2]
        hub_next = self.lst_choose[-1][1]
        while hub_next.name != self.start_name:
            for _, hn, hs in self.lst_choose:
                if hub_next == hs:
                    self.lst_solve.append((hub_solve.x,hub_solve.y))
                    hub_solve = hs
                    hub_next = hn
        self.lst_solve.append((hub_solve.x,hub_solve.y))
        self.lst_solve.append((hub_next.x,hub_next.y))
        self.lst_solve = self.lst_solve[::-1]
        print(self.lst_solve)



    
    def dijkstrar(self, hub, cost):
        if hub.name == self.end_name:
            return 
        if not hub.visited:
            for link in hub.lst_link:
                link.cost = cost
                if link.zone == "normal":
                    link.cost += 1
                    self.lst_cost.append((link.cost,hub,link))
                if link.zone == "prioritie":
                    link.cost += 0
                    self.lst_cost.append((link.cost,hub,link))
                if link.zone == "restricted":
                    link.cost += 2
                    self.lst_cost.append((link.cost,hub,link))
        min_cost = self.lst_cost[0][0]
        for i in range(len(self.lst_cost)):
            if self.lst_cost[i][0] <= min_cost:
                min_cost = self.lst_cost[i][0]
                index_min = i
        hub.visited = True
        new_hub = self.lst_cost[index_min][2]
        self.lst_choose.append((min_cost, self.lst_cost[index_min][1], new_hub))
        for element,h,nh in self.lst_cost:
            print(element,h.name ,nh.name)
        print(f"new_hub : ({new_hub.name})")
        print("=" * 30)
        self.lst_cost.pop(index_min)
        self.dijkstrar(new_hub, min_cost)


def main(dico):
    maps = Map(dico)
    maps.solve()
    for element in maps.lst_choose:
        print(element)
    # print(maps.lst_choose)

main(
    {'nb_drones': 25, 
    'start': {'name': 'start', 'x': 0, 'y': 0, 'color': 'green', 'max_drones': '25'}, 
    'end': {'name': 'impossible_goal', 'x': 21, 'y': 0, 'color': 'rainbow', 'max_drones': '25'}, 
    'hub': {
        'start': {'x': 0, 'y': 0}, 
        'gate_hell1': {'x': 1, 'y': 0, 'color': 'red', 'max_drones': '1'}, 
        'gate_hell2': {'x': 2, 'y': 0, 'color': 'red', 'max_drones': '1'}, 
        'gate_hell3': {'x': 3, 'y': 0, 'color': 'red', 'max_drones': '1'}, 
        'gate_hell4': {'x': 4, 'y': 0, 'color': 'red', 'max_drones': '1'}, 
        'gate_hell5': {'x': 5, 'y': 0, 'color': 'red', 'max_drones': '1'}, 
        'maze_trap_a1': {'x': 1, 'y': 1, 'color': 'purple'}, 
        'maze_trap_a2': {'x': 2, 'y': 1, 'color': 'purple'}, 
        'maze_trap_a3': {'x': 3, 'y': 1, 'color': 'purple'}, 
        'maze_dead_a': {'x': 4, 'y': 1, 'color': 'black'}, 
        'maze_trap_b1': {'x': 1, 'y': -1, 'color': 'purple'}, 
        'maze_trap_b2': {'x': 2, 'y': -1, 'color': 'purple'}, 
        'maze_trap_b3': {'x': 3, 'y': -1, 'color': 'purple'}, 
        'maze_dead_b': {'x': 4, 'y': -1, 'color': 'black'}, 
        'maze_loop1': {'x': 1, 'y': 2, 'zone': 'restricted', 'color': 'brown'}, 
        'maze_loop2': {'x': 2, 'y': 2, 'zone': 'restricted', 'color': 'brown'}, 
        'maze_loop3': {'x': 3, 'y': 2, 'zone': 'restricted', 'color': 'brown'}, 
        'maze_loop4': {'x': 4, 'y': 2, 'zone': 'restricted', 'color': 'brown'}, 
        'maze_loop5': {'x': 5, 'y': 2, 'zone': 'restricted', 'color': 'brown'}, 
        'maze_loop6': {'x': 5, 'y': 1, 'zone': 'restricted', 'color': 'brown'}, 
        'micro_gate1': {'x': 6, 'y': 0, 'color': 'orange', 'max_drones': '1'}, 
        'micro_gate2': {'x': 7, 'y': 0, 'color': 'orange', 'max_drones': '1'}, 
        'micro_gate3': {'x': 8, 'y': 0, 'color': 'orange', 'max_drones': '1'}, 
        'overflow_hell1': {'x': 6, 'y': 1, 'zone': 'restricted', 'color': 'maroon', 'max_drones': '2'}, 
        'overflow_hell2': {'x': 7, 'y': 1, 'zone': 'restricted', 'color': 'maroon', 'max_drones': '2'}, 
        'overflow_hell3': {'x': 8, 'y': 1, 'zone': 'restricted', 'color': 'maroon', 'max_drones': '2'}, 
        'overflow_hell4': {'x': 6, 'y': -1, 'zone': 'restricted', 'color': 'maroon', 'max_drones': '2'}, 
        'overflow_hell5': {'x': 7, 'y': -1, 'zone': 'restricted', 'color': 'maroon', 'max_drones': '2'}, 
        'overflow_hell6': {'x': 8, 'y': -1, 'zone': 'restricted', 'color': 'maroon', 'max_drones': '2'}, 
        'false_hope1': {'x': 9, 'y': 0, 'zone': 'priority', 'color': 'gold', 'max_drones': '3'}, 
        'false_hope2': {'x': 10, 'y': 0, 'zone': 'priority', 'color': 'gold', 'max_drones': '2'}, 
        'false_hope3': {'x': 11, 'y': 0, 'zone': 'priority', 'color': 'gold', 'max_drones': '1'}, 
        'priority_trap1': {'x': 9, 'y': 1, 'zone': 'priority', 'color': 'gold'}, 
        'priority_trap2': {'x': 10, 'y': 1, 'zone': 'priority', 'color': 'gold'}, 
        'priority_dead': {'x': 11, 'y': 1, 'color': 'black'}, 
        'priority_trap3': {'x': 9, 'y': -1, 'zone': 'priority', 'color': 'gold'}, 
        'priority_trap4': {'x': 10, 'y': -1, 'zone': 'priority', 'color': 'gold'}, 
        'priority_dead2': {'x': 11, 'y': -1, 'color': 'black'}, 
        'conv_restricted1': {'x': 12, 'y': 2, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted2': {'x': 13, 'y': 2, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted3': {'x': 14, 'y': 2, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted4': {'x': 12, 'y': 0, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted5': {'x': 13, 'y': 0, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted6': {'x': 14, 'y': 0, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted7': {'x': 12, 'y': -2, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted8': {'x': 13, 'y': -2, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'conv_restricted9': {'x': 14, 'y': -2, 'zone': 'restricted', 'color': 'darkred', 'max_drones': '1'}, 
        'final_merge': {'x': 15, 'y': 0, 'color': 'violet', 'max_drones': '5'}, 
        'final_torture1': {'x': 16, 'y': 0, 'color': 'crimson', 'max_drones': '2'}, 
        'final_torture2': {'x': 17, 'y': 0, 'color': 'crimson', 'max_drones': '1'}, 
        'final_torture3': {'x': 18, 'y': 0, 'color': 'crimson', 'max_drones': '1'}, 
        'final_torture4': {'x': 19, 'y': 0, 'color': 'crimson', 'max_drones': '1'}, 
        'final_torture5': {'x': 20, 'y': 0, 'color': 'crimson', 'max_drones': '1'}, 
        'impossible_goal': {'x': 21, 'y': 0}
        }, 
    'link': [
        {'hub1': 'start', 'hub2': 'gate_hell1', 'max_link_capacity': '1'}, 
        {'hub1': 'gate_hell1', 'hub2': 'gate_hell2', 'max_link_capacity': '1'}, 
        {'hub1': 'gate_hell2', 'hub2': 'gate_hell3', 'max_link_capacity': '1'}, 
        {'hub1': 'gate_hell3', 'hub2': 'gate_hell4', 'max_link_capacity': '1'}, 
        {'hub1': 'gate_hell4', 'hub2': 'gate_hell5', 'max_link_capacity': '1'}, 
        {'hub1': 'gate_hell1', 'hub2': 'maze_trap_a1'}, 
        {'hub1': 'gate_hell2', 'hub2': 'maze_trap_b1'}, 
        {'hub1': 'gate_hell3', 'hub2': 'maze_loop1'}, 
        {'hub1': 'maze_trap_a1', 'hub2': 'maze_trap_a2'}, 
        {'hub1': 'maze_trap_a2', 'hub2': 'maze_trap_a3'}, 
        {'hub1': 'maze_trap_a3', 'hub2': 'maze_dead_a'}, 
        {'hub1': 'maze_trap_b1', 'hub2': 'maze_trap_b2'}, 
        {'hub1': 'maze_trap_b2', 'hub2': 'maze_trap_b3'}, 
        {'hub1': 'maze_trap_b3', 'hub2': 'maze_dead_b'}, 
        {'hub1': 'maze_loop1', 'hub2': 'maze_loop2'}, 
        {'hub1': 'maze_loop2', 'hub2': 'maze_loop3'}, 
        {'hub1': 'maze_loop3', 'hub2': 'maze_loop4'}, 
        {'hub1': 'maze_loop4', 'hub2': 'maze_loop5'}, 
        {'hub1': 'maze_loop5', 'hub2': 'maze_loop6'}, 
        {'hub1': 'maze_loop6', 'hub2': 'maze_loop1'}, 
        {'hub1': 'maze_trap_a2', 'hub2': 'micro_gate1'}, 
        {'hub1': 'maze_trap_b2', 'hub2': 'micro_gate1'}, 
        {'hub1': 'maze_loop3', 'hub2': 'micro_gate2'}, 
        {'hub1': 'gate_hell5', 'hub2': 'micro_gate1'}, 
        {'hub1': 'micro_gate1', 'hub2': 'micro_gate2'}, 
        {'hub1': 'micro_gate2', 'hub2': 'micro_gate3'}, 
        {'hub1': 'micro_gate1', 'hub2': 'overflow_hell1'}, 
        {'hub1': 'micro_gate2', 'hub2': 'overflow_hell2'}, 
        {'hub1': 'micro_gate3', 'hub2': 'overflow_hell3'}, 
        {'hub1': 'micro_gate1', 'hub2': 'overflow_hell4'}, 
        {'hub1': 'micro_gate2', 'hub2': 'overflow_hell5'}, 
        {'hub1': 'micro_gate3', 'hub2': 'overflow_hell6'}, 
        {'hub1': 'overflow_hell1', 'hub2': 'overflow_hell2'}, 
        {'hub1': 'overflow_hell2', 'hub2': 'overflow_hell3'}, 
        {'hub1': 'overflow_hell4', 'hub2': 'overflow_hell5'}, 
        {'hub1': 'overflow_hell5', 'hub2': 'overflow_hell6'}, 
        {'hub1': 'overflow_hell3', 'hub2': 'false_hope1'}, 
        {'hub1': 'overflow_hell6', 'hub2': 'false_hope1'}, 
        {'hub1': 'micro_gate3', 'hub2': 'false_hope1'}, 
        {'hub1': 'false_hope1', 'hub2': 'false_hope2'}, 
        {'hub1': 'false_hope2', 'hub2': 'false_hope3'}, 
        {'hub1': 'false_hope1', 'hub2': 'priority_trap1'}, 
        {'hub1': 'false_hope2', 'hub2': 'priority_trap2'}, 
        {'hub1': 'false_hope3', 'hub2': 'priority_dead'}, 
        {'hub1': 'false_hope1', 'hub2': 'priority_trap3'}, 
        {'hub1': 'false_hope2', 'hub2': 'priority_trap4'}, 
        {'hub1': 'false_hope3', 'hub2': 'priority_dead2'}, 
        {'hub1': 'priority_trap1', 'hub2': 'priority_trap2'}, 
        {'hub1': 'priority_trap3', 'hub2': 'priority_trap4'},
        {'hub1': 'false_hope3', 'hub2': 'conv_restricted1'}, 
        {'hub1': 'false_hope3', 'hub2': 'conv_restricted4'}, 
        {'hub1': 'false_hope3', 'hub2': 'conv_restricted7'}, 
        {'hub1': 'conv_restricted1', 'hub2': 'conv_restricted2'}, 
        {'hub1': 'conv_restricted2', 'hub2': 'conv_restricted3'},
        {'hub1': 'conv_restricted4', 'hub2': 'conv_restricted5'}, 
        {'hub1': 'conv_restricted5', 'hub2': 'conv_restricted6'}, 
        {'hub1': 'conv_restricted7', 'hub2': 'conv_restricted8'}, 
        {'hub1': 'conv_restricted8', 'hub2': 'conv_restricted9'}, 
        {'hub1': 'conv_restricted3', 'hub2': 'final_merge'}, 
        {'hub1': 'conv_restricted6', 'hub2': 'final_merge'}, 
        {'hub1': 'conv_restricted9', 'hub2': 'final_merge'}, 
        {'hub1': 'final_merge', 'hub2': 'final_torture1'}, 
        {'hub1': 'final_torture1', 'hub2': 'final_torture2'}, 
        {'hub1': 'final_torture2', 'hub2': 'final_torture3'}, 
        {'hub1': 'final_torture3', 'hub2': 'final_torture4'}, 
        {'hub1': 'final_torture4', 'hub2': 'final_torture5'}, 
        {'hub1': 'final_torture5', 'hub2': 'impossible_goal'},
        {'hub1': 'overflow_hell1', 'hub2': 'conv_restricted1'}, 
        {'hub1': 'overflow_hell4', 'hub2': 'conv_restricted7'}, 
        {'hub1': 'priority_trap1', 'hub2': 'conv_restricted4'}]}
)

