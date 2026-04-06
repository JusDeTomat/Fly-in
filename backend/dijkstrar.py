class Ship_solve:
    def __init__(self, id):
        self.id = id
        self.hub_solve = 0
        self.hub_next = 0
        self.lst_solve = []
        self.finish = False
        self.stuck = False

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
        self.max_size = False
        self.nb_in = 0

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
            self.lst_ship.append(Ship_solve(i))
            
    
    def solve(self):

        self.finish_solve = True
        for hub in self.lst_hub:
            if hub.name == self.end_name:
                hub_start = hub
        self.dijkstrar(hub_start,0)
        for ship in self.lst_ship:
            ship.hub_solve = self.lst_choose[-1][2]
            ship.hub_next = self.lst_choose[-1][1]
            ship.lst_solve.append((ship.hub_solve.x, ship.hub_solve.y))
        while self.finish_solve:
            for ship in self.lst_ship:
                if ship.stuck:
                    print(ship.id)
                    ship.hub_solve.nb_in += 1
                    if ship.hub_solve.max_in <= ship.hub_solve.nb_in:
                        ship.hub_solve.max_size = True
        
            for ship in self.lst_ship:
                if not ship.stuck:
                    if ship.hub_next.name == self.end_name:
                        ship.hub_solve = ship.hub_next
                        ship.finish = True
                    if not ship.finish:
                        for _, hn, hs in self.lst_choose:
                            if ship.hub_next == hs and not ship.hub_next.max_size and not hn.max_size:
                                ship.hub_solve = hs
                                ship.hub_next = hn
                                ship.hub_solve.nb_in += 1
                                if ship.hub_solve.zone == 'restricted':
                                    ship.stuck = True
                                if ship.hub_solve.max_in <= ship.hub_solve.nb_in:
                                    ship.hub_solve.max_size = True
                else:
                    ship.stuck = False
                print(ship.id, ship.hub_solve.name)
                ship.lst_solve.append((ship.hub_solve.x, ship.hub_solve.y))
            for hub in self.lst_hub:
                hub.nb_in = 0
                hub.max_size = False
            i = 0
            for ship in self.lst_ship:
                print(ship.finish)
                if not ship.finish:
                    break
                i += 1
                if i >= len(self.lst_ship):
                    self.finish_solve = False

        for ship in self.lst_ship:
            self.lst_solve.append(ship.lst_solve)
        return self.lst_solve



    
    def dijkstrar(self, hub, cost):
        if hub.name == self.start_name:
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
        self.lst_cost.pop(index_min)
        self.dijkstrar(new_hub, min_cost)

