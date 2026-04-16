from typing import Any, Dict, List, Tuple
from src.enums import Cost


class Ship_solve:
    """Represents a ship in the solving process.

    Attributes:
        id (int): Unique identifier for the ship.
        hub_solve: Current hub the ship is at.
        hub_next: Next hub the ship is moving to.
        lst_solve: List of positions (x, y) the ship has visited.
        finish (bool): Whether the ship has reached the end.
        int_finish (int): Internal finish counter.
        stuck (bool): Whether the ship is stuck.
        lst_output: List of output strings for the ship.
        x, y (float): Current position coordinates.
    """
    def __init__(self, id: int) -> None:
        self.id = id
        self.hub_solve: Any = 0
        self.hub_next: Any = 0
        self.lst_solve: List[Tuple[float, float]] = []
        self.finish = False
        self.int_finish = 0
        self.stuck = False
        self.lst_output: List[Any] = []
        self.x = 0
        self.y = 0


class Hub:
    """Represents a hub in the map.

    Attributes:
        lst_link: List of links connected to this hub.
        name (str): Name of the hub.
        visited (bool): Whether the hub has been visited in Dijkstra.
        x, y (int): Coordinates of the hub.
        zone (str): Zone type of the hub.
        nb_in (int): Number of ships currently in the hub.
        max_in (int): Maximum number of ships allowed.
        max_size (bool): Whether the hub is at max capacity.
        come (int): Number of ships coming to the hub.
    """
    def __init__(self, name: str, x: int,
                 y: int, zone: str, max_drone: int) -> None:
        self.lst_link: List[Any] = []
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


class Link:
    """Represents a link between two hubs.

    Attributes:
        hub1, hub2: The two hubs connected by this link.
        max_in (int): Maximum capacity of the link.
        nb_in (int): Current number of ships on the link.
        max_size (bool): Whether the link is at max capacity.
        x, y (float): Midpoint coordinates of the link.
    """
    def __init__(self, hub1: Any, hub2: Any, max_in: int) -> None:
        self.hub1 = hub1
        self.hub2 = hub2
        self.max_in = max_in
        self.nb_in = 0
        self.max_size = self.max_in <= self.nb_in
        self.x = (hub1.x + hub2.x) / 2
        self.y = (hub1.y + hub2.y) / 2


class Map:
    """Represents the entire map with hubs, links, and ships.

    Handles parsing the input dictionary, creating hubs and links,
    adding ships, and solving the pathfinding problem.
    """
    def __init__(self, dico_info: Dict[str, Any]) -> None:
        self.dico = dico_info
        self.start_name = dico_info['start']['name']
        self.end_name = dico_info['end']['name']
        self.lst_hub: List[Hub] = []
        self.lst_link: List[Link] = []
        self.add_all_hub()
        self.lst_ship: List[Ship_solve] = []
        self.add_ship(self.dico['nb_drones'])
        self.finish_solve = False
        self.lst_solve: List[List[Tuple[float, float]]] = []
        self.lst_cost: List[Tuple[float, Any]] = []
        self.lst_choose: List[Tuple[float, Link]] = []
        self.lst_output: List[List[Any]] = []

    def add_all_hub(self) -> None:
        """Create and add all hubs from the input dictionary."""
        key_hub = self.dico["hub"].keys()
        link = self.dico["link"]
        for name_hub in key_hub:
            if (name_hub == self.start_name
               or name_hub == self.end_name):
                hub = Hub(
                    name_hub,
                    self.dico['hub'][name_hub]['x'],
                    self.dico['hub'][name_hub]['y'],
                    self.dico['hub'][name_hub].get('zone', 'normal'),
                    self.dico['hub'][name_hub].get('max_drones',
                                                   self.dico['nb_drones'])
                )
            else:
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
                    max_size = int(element.get("max_link_capacity", 1))
                    for hub2 in self.lst_hub:
                        if hub2.name == element['hub1']:
                            link_in = False
                            for links in self.lst_link:
                                if hub == links.hub1 and hub2 == links.hub2:
                                    link_in = True
                            if not link_in:
                                self.lst_link.append(Link(hub, hub2, max_size))
        for hub in self.lst_hub:
            for element in link:
                if element['hub2'] == hub.name:
                    max_size = int(element.get("max_link_capacity", 1))
                    for hub2 in self.lst_hub:
                        if hub2.name == element['hub1']:
                            for links in self.lst_link:
                                if hub == links.hub1 and hub2 == links.hub2:
                                    hub.lst_link.append(links)

    def add_ship(self, nb_drones: int) -> None:
        """Add the specified number of ships to the map.

        Args:
            nb_drones (int): Number of ships to add.
        """
        for i in range(nb_drones):
            self.lst_ship.append(Ship_solve(i + 1))

    def solve(self) -> List[List[Tuple[float, float]]]:
        """Solve the pathfinding problem for all ships.

        Uses Dijkstra-like algorithm to find paths from start to end,
        considering hub capacities and zones.

        Returns:
            List of lists of (x, y) positions for each ship.

        Raises:
            ValueError: If no path is found.
        """
        try:
            self.finish_solve = True
            for hub in self.lst_hub:
                if hub.name == self.end_name:
                    hub_start = hub
                hub.visited = False
            self.dijkstrar(hub_start, 0.0)
            for ship in self.lst_ship:
                for cost, link in self.lst_choose:
                    hs = link.hub2
                    hn = link.hub1
                    if hs.name == self.start_name and not hs.max_size:
                        ship.hub_solve = hs
                        ship.hub_next = hn
                        ship.lst_solve.append((ship.hub_solve.x,
                                               ship.hub_solve.y))
            while self.finish_solve:
                for ship in self.lst_ship:
                    if ship.stuck:
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
                            for cost, link in self.lst_choose:
                                hs = link.hub2
                                hn = link.hub1
                                new_link = link
                                min_cost = cost
                                if (ship.hub_next == hs
                                   and not hs.max_size
                                   and not new_link.max_size
                                   and not (hn.come >= hn.max_in)
                                   and play == 0):
                                    if not (hn.max_size):
                                        for costa, links in self.lst_choose:
                                            hsa = links.hub2
                                            hna = links.hub1
                                            if (hs == hsa
                                               and not hna.max_size
                                               and not hsa.max_size
                                               and not links.max_size
                                               and costa <= min_cost):
                                                hs = hsa
                                                hn = hna
                                                min_cost = costa
                                                new_link = links
                                    ship.x = (ship.hub_solve.x + hs.x) / 2
                                    ship.y = (ship.hub_solve.y + hs.y) / 2
                                    ship.hub_solve = hs
                                    ship.hub_next = hn
                                    play = 1
                                    new_link.nb_in += 1
                                    if not ship.stuck:
                                        ship.hub_solve.nb_in += 1
                                    if new_link.nb_in >= new_link.max_in:
                                        new_link.max_size = True
                                    if ship.hub_solve.zone == "restricted":
                                        ship.stuck = True
                                    if (ship.hub_solve.max_in <=
                                       ship.hub_solve.nb_in):
                                        ship.hub_solve.max_size = True
                            if not ship.stuck:
                                ship.hub_next.come += 1
                    else:
                        ship.stuck = False
                    if not ship.stuck:
                        ship.lst_solve.append((ship.hub_solve.x,
                                               ship.hub_solve.y))
                    else:
                        ship.lst_solve.append((ship.x, ship.y))
                    if ship.int_finish <= 1:
                        ship.lst_output.append(f"D{ship.id}-"
                                               f"{ship.hub_solve.name}")
                    else:
                        ship.lst_output.append(None)
                for hub in self.lst_hub:
                    hub.come = 0
                    hub.nb_in = 0
                    if hub.max_in != 0:
                        hub.max_size = False
                for link in self.lst_link:
                    link.nb_in = 0
                    link.max_size = False
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

    def dijkstrar(self, hub: Any, cost: float) -> None:
        """Run the Dijkstra algorithm from the given hub.

        Args:
            hub: Starting hub.
            cost (float): Initial cost.
        """
        while hub.name != self.start_name:
            if not hub.visited:
                for link in hub.lst_link:
                    link.hub1.cost = cost
                    if link.hub2.zone == "priority" and link.hub2.max_in > 0:
                        link.hub1.cost += Cost.PRIORITY.value - 0.1
                        self.lst_cost.append((link.hub1.cost, link))
                    if link.hub2.zone == "normal" and link.hub2.max_in > 0:
                        link.hub1.cost += Cost.NORMAL.value
                        self.lst_cost.append((link.hub1.cost, link))
                    if link.hub2.zone == "restricted" and link.hub2.max_in > 0:
                        link.hub1.cost += Cost.RESTRICTED.value
                        self.lst_cost.append((link.hub1.cost, link))
            min_cost = self.lst_cost[0][0]
            for i in range(len(self.lst_cost)):
                if self.lst_cost[i][0] <= min_cost:
                    min_cost = self.lst_cost[i][0]
                    index_min = i
            hub.visited = True
            new_hub = self.lst_cost[index_min][1].hub2
            self.lst_choose.append((min_cost, self.lst_cost[index_min][1]))
            self.lst_cost.pop(index_min)
            hub = new_hub
            cost = min_cost
