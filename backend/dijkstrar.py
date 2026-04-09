class Ship_solve:
    def __init__(self, id):
        self.id = id
        self.hub_solve = 0
        self.hub_next = 0
        self.lst_solve = []
        self.finish = False
        self.int_finish = 0
        self.stuck = False
        self.lst_output = []

class Hub:
    def __init__(self, name, x, y, zone, max_drone):
        self.lst_link = []
        self.name = name
        self.visited = False
        self.x = x
        self.y = y
        self.zone = zone
        self.nb_in = 0
        self.max_in = int(max_drone)
        self.cost = 0
        self.nb_in = 0
        self.max_size = self.max_in <= self.nb_in
        self.come = 0


class Map:
    def __init__(self, dico_info):
        self.dico = dico_info
        self.lst_hub = []
        self.add_all_hub()
        self.lst_ship = []
        self.add_ship(self.dico['nb_drones'])
        self.start_name = dico_info['start']['name']
        self.end_name = dico_info['end']['name']
        self.finish_solve = False
        self.lst_solve = []
        self.lst_cost = []
        self.lst_choose = []
        self.lst_output = []

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
                if element['hub2'] == hub.name:
                    for hub2 in self.lst_hub:
                        if hub2.name == element['hub1']:
                            hub.lst_link.append(hub2)
    
    def add_ship(self, nb_drones):
        for i in range(nb_drones):
            self.lst_ship.append(Ship_solve(i + 1))
            
    
    def solve(self):
        try :
            self.finish_solve = True
            for hub in self.lst_hub:
                if hub.name == self.end_name:
                    hub_start = hub
                hub.visited = False
            self.dijkstrar(hub_start,0)
            for ship in self.lst_ship:
                for cost, hn, hs in self.lst_choose:  
                    if hs.name == self.start_name and not hs.max_size:
                        ship.hub_solve = hs
                        ship.hub_next = hn
                        ship.lst_solve.append((ship.hub_solve.x, ship.hub_solve.y))
            while self.finish_solve:
                for ship in self.lst_ship:
                    if ship.stuck:
                        ship.hub_solve.nb_in += 1
                        if ship.hub_solve.max_in <= ship.hub_solve.nb_in:
                                    ship.hub_solve.max_size = True

                for ship in self.lst_ship:
                    if not ship.stuck:
                        if ship.hub_next.name == self.end_name:
                            ship.hub_solve = ship.hub_next
                            ship.finish = True
                            ship.int_finish += 1
                        if not ship.finish:
                            play = 0
                            for cost, hn, hs in self.lst_choose:
                                min_cost = cost
                                if ship.hub_next == hs and not hs.max_size and not (hn.come >= hn.max_in) and play == 0:
                                    if not (hn.max_size):
                                        for costa, hna, hsa in self.lst_choose:
                                            if hs == hsa and not hna.max_size and not hsa.max_size and costa <= min_cost:
                                                hs = hsa
                                                hn = hna
                                                min_cost = costa
                                    ship.hub_solve = hs
                                    ship.hub_next = hn
                                    play = 1
                                    ship.hub_solve.nb_in += 1
                                    if ship.hub_solve.zone == 'restricted':
                                        ship.stuck = True
                                    if ship.hub_solve.max_in <= ship.hub_solve.nb_in:
                                        ship.hub_solve.max_size = True
                            if not ship.stuck:
                                ship.hub_next.come += 1
                    else:
                        ship.stuck = False
                    ship.lst_solve.append((ship.hub_solve.x, ship.hub_solve.y))
                    if ship.int_finish <= 1:
                        ship.lst_output.append(f"D{ship.id}-{ship.hub_solve.name}")
                    else:
                        ship.lst_output.append(None)
                for hub in self.lst_hub:
                    hub.come = 0
                    hub.nb_in = 0
                    if hub.max_in != 0:
                        hub.max_size = False
                i = 0
                for ship in self.lst_ship:
                    if not ship.finish:
                        break
                    i += 1
                    if i >= len(self.lst_ship):
                        self.finish_solve = False

            for ship in self.lst_ship:
                self.lst_solve.append(ship.lst_solve)
                self.lst_output.append(ship.lst_output)

            return self.lst_solve
        except IndexError:
            raise ValueError("No path found")



    
    def dijkstrar(self, hub, cost):

        while hub.name != self.start_name:
            if not hub.visited:
                for link in hub.lst_link:
                    link.cost = cost
                    if link.zone == "priority" and link.max_in > 0:
                        link.cost += 0.9
                        self.lst_cost.append((link.cost,hub,link))
                    if link.zone == "normal" and link.max_in > 0:
                        link.cost += 1
                        self.lst_cost.append((link.cost,hub,link))
                    if link.zone == "restricted" and link.max_in > 0:
                        link.cost += 2.5
                        self.lst_cost.append((link.cost,hub,link))
            min_cost = self.lst_cost[0][0]
            for i in range(len(self.lst_cost)):
                if self.lst_cost[i][0] <= min_cost:
                    min_cost = self.lst_cost[i][0]
                    index_min = i
            hub.visited = True
            new_hub = self.lst_cost[index_min][2]
            self.lst_choose.append((min_cost, self.lst_cost[index_min][1], new_hub))
            self.lst_cost.pop(index_min)
            hub = new_hub
            cost = min_cost