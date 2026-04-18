from typing import Dict, Any, List, Tuple
import pyray as rl
import math
from src.enums import Model


class Ship:
    """Represents a ship in the visual simulation.

    Attributes:
        ship_id (int): ID of the ship.
        id_path (int): Current path index.
        t (float): Interpolation parameter for movement.
        model: 3D model of the ship.
        position: Current 3D position.
        angle (float): Rotation angle.
        end (bool): Whether the ship has finished its path.
    """
    def __init__(self, id: int, model: Any) -> None:
        self.ship_id: int = id
        self.id_path: int = 1
        self.t: float = 0.005
        self.model: Any = model
        self.position: Any = rl.Vector3(0, 1.5, 0)
        self.angle: float = 90.0
        self.end: bool = False


class Visual:
    """Handles the 3D visualization of the map and ships.

    Manages drawing hubs, links, ships, and the overall scene.
    """
    def __init__(self, dico_info: Dict[str, Any],
                 solve: List[List[Tuple[float, float]]],
                 model: Dict[str, Any]) -> None:

        self.dico_info: Dict[str, Any] = dico_info
        self.path: List[List[Tuple[float, float]]] = solve
        self.angle: float = 0
        self.level_ves: int = 0
        self.model: Dict[str, Any] = model
        self.lst_ship: List[Ship] = []
        self.add_ship()
        self.speed: float = 0.01
        self.stop: bool = True

    def add_ship(self) -> None:
        """Add ships to the visual based on the number of drones."""
        for i in range(self.dico_info['nb_drones']):
            self.lst_ship.append(Ship(i, self.model["ship"]))
        self.lst_ship

    def draw_map(self) -> None:
        """Draw all hubs and their models on the map."""
        x = int(self.dico_info["start"]["x"])
        y = int(self.dico_info["start"]["y"])
        rl.draw_model_ex(
                        self.model["start"],
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 1, 0),
                        -90,
                        rl.Vector3(0.001, 0.001, 0.001),
                        rl.WHITE
                    )
        x = int(self.dico_info["end"]["x"])
        y = int(self.dico_info["end"]["y"])
        rl.draw_model_ex(
                        self.model["end"],
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        0,
                        rl.Vector3(0.03, 0.03, 0.03),
                        rl.WHITE
                    )
        key_hub = self.dico_info["hub"].keys()
        for element in key_hub:
            x = int(self.dico_info["hub"][element]["x"])
            y = int(self.dico_info["hub"][element]["y"])
            mode = self.dico_info["hub"][element].get("zone", "normal")
            color = self.dico_info['hub'][element].get('color',
                                                       'WHITE').upper()
            rl.draw_sphere(rl.Vector3(x * 3, 1, y * 3), 0.3,
                           self.convert_color(color))
            if (mode == "restricted"):
                rl.draw_model_ex(
                        self.model["neptune"],
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.01, 0.01, 0.01),
                        rl.WHITE
                    )
            elif (mode == "blocked"):
                rl.draw_model_ex(
                        self.model["sun"],
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.05, 0.05, 0.05),
                        rl.WHITE
                    )
            elif (mode == "priority"):
                rl.draw_model_ex(
                        self.model["moon"],
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.01, 0.01, 0.01),
                        rl.WHITE
                    )
            elif (element != self.dico_info["start"]["name"]
                  and element != self.dico_info["end"]["name"]):
                rl.draw_model_ex(
                        self.model["saturn"],
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 20),
                        self.angle,
                        rl.Vector3(0.001, 0.001, 0.001),
                        rl.WHITE
                    )

    def draw_link(self) -> None:
        """Draw all links between hubs."""
        link = self.dico_info["link"]
        for element in link:
            x1 = int(self.dico_info["hub"][element['hub1']]["x"])
            y1 = int(self.dico_info["hub"][element['hub1']]["y"])
            x2 = int(self.dico_info["hub"][element['hub2']]["x"])
            y2 = int(self.dico_info["hub"][element['hub2']]["y"])
            rl.draw_line_3d(rl.Vector3(x1 * 3, 0, y1 * 3),
                            rl.Vector3(x2 * 3, 0, y2 * 3), rl.WHITE)

    def convert_color(self, color: str) -> Any:
        """Convert a color name to Raylib color object.

        Args:
            color (str): Name of the color.

        Returns:
            Raylib color object.

        Raises:
            ValueError: If color is not recognized.
        """
        match color:
            case "RED":
                return rl.RED
            case "ORANGE":
                return rl.ORANGE
            case "WHITE":
                return rl.WHITE
            case "CRIMSON":
                return (220, 20, 60, 255)
            case "VIOLET":
                return rl.VIOLET
            case "DARKRED":
                return (139, 0, 0, 255)
            case "BLACK":
                return rl.BLACK
            case "GOLD":
                return rl.GOLD
            case "MAROON":
                return rl.MAROON
            case "BROWN":
                return rl.BROWN
            case "PURPLE":
                return rl.PURPLE
            case "YELLOW":
                return rl.YELLOW
            case "BLUE":
                return rl.BLUE
            case "GREEN":
                return rl.GREEN
            case "DARKGREEN":
                return rl.DARKGREEN
            case "DARKPURPLE":
                return rl.DARKPURPLE
            case "CYAN":
                return (43, 255, 255, 255)
            case "LIME":
                return rl.LIME
            case "MAGENTA":
                return rl.MAGENTA
            case "RAINBOW":
                return (225, 255, 250, 255)
        return rl.WHITE

    def draw_moove_ship(self) -> None:
        """Draw and update the positions of moving ships."""
        stop = 0
        end = 0
        for ship in self.lst_ship:
            if ship.end:
                pass
            elif self.stop:
                ship.angle = 90
                rl.draw_model_ex(
                            ship.model,
                            ship.position,
                            rl.Vector3(0, 1, 0),
                            ship.angle,
                            rl.Vector3(0.05, 0.05, 0.05),
                            rl.WHITE
                        )
            else:
                x1, y1 = self.path[ship.ship_id][ship.id_path - 1]
                x2, y2 = self.path[ship.ship_id][ship.id_path]
                ship.position.x = x1 * 3 + (x2 * 3 - x1 * 3) * ship.t
                ship.position.z = y1 * 3 + (y2 * 3 - y1 * 3) * ship.t
                direction = rl.Vector3(
                    x2 * 3 - ship.position.x,
                    0,
                    y2 * 3 - ship.position.z
                )
                direction = rl.vector3_normalize(direction)
                ship.angle = math.degrees(math.atan2(direction.x, direction.z))
                rl.draw_model_ex(
                                ship.model,
                                ship.position,
                                rl.Vector3(0, 1, 0),
                                ship.angle,
                                rl.Vector3(0.05, 0.05, 0.05),
                                rl.WHITE
                            )
                ship.t += self.speed
                if (ship.t >= 1):
                    ship.t = 0.005
                    if (ship.id_path + 1 <= len(self.path[0]) - 1):
                        ship.id_path += 1
                        stop = 1
                    else:
                        ship.end = True
                        end = 1
        if end:
            self.end = True
        if stop:
            self.stop = True


def main_visual(
    dico: Dict[str, Any],
    solve: List[List[Tuple[float, float]]]
) -> None:
    """Main function to start the visual simulation.

    Args:
        dico: Parsed input dictionary.
        solve: Solved paths for ships.
    """
    rl.set_trace_log_level(7)
    rl.init_window(1800, 1000, "Fly-In")

    camera = rl.Camera3D(
        rl.Vector3(0.0, 2.0, 6.0),
        rl.Vector3(0.0, 1.0, 0.0),
        rl.Vector3(0.0, 1.0, 0.0),
        60.0,
        rl.CameraProjection.CAMERA_PERSPECTIVE
    )

    rl.set_target_fps(60)
    model = {}
    background = rl.load_model(Model.BLACK_HOLE.value)
    model["start"] = rl.load_model(Model.START.value)
    model["ship"] = rl.load_model(Model.SHIP.value)
    model["neptune"] = rl.load_model(Model.NEPTUNE.value)
    model["saturn"] = rl.load_model(Model.SATURN.value)
    model["moon"] = rl.load_model(Model.MOON.value)
    model["sun"] = rl.load_model(Model.SUN.value)
    model["end"] = rl.load_model(Model.END.value)

    texture = rl.load_texture(Model.SKYBOX.value)
    mesh = rl.gen_mesh_sphere(1.0, 32, 100)
    sphere = rl.load_model_from_mesh(mesh)
    sphere.materials[0].maps[
        rl.MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = texture

    vis = Visual(dico, solve, model)

    while not rl.window_should_close():
        count = 0
        mouse = rl.get_mouse_position()
        ray = rl.get_screen_to_world_ray(mouse, camera)
        for ship in vis.lst_ship:
            pos = ship.position
            box = rl.BoundingBox(
                rl.Vector3(pos.x - 0.3, pos.y - 0.3, pos.z - 0.3),
                rl.Vector3(pos.x + 0.3, pos.y + 0.3, pos.z + 0.3)
            )
            hit = rl.get_ray_collision_box(ray, box)

            if hit.hit:
                count += 1

        if (rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_LEFT)
           or rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_RIGHT)):
            rl.update_camera(camera, rl.CameraMode.CAMERA_FREE)

        elif rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            if vis.stop:
                vis.stop = False

        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            if vis.speed < 1:
                vis.speed += 0.01

        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
            if vis.speed > 0.01:
                vis.speed -= 0.01

        if rl.is_key_pressed(rl.KeyboardKey.KEY_R):
            for ship in vis.lst_ship:
                if ship.id_path > 1:
                    ship.id_path -= 1
        rl.begin_drawing()
        rl.clear_background((0, 0, 0, 255))

        rl.begin_mode_3d(camera)
        rl.draw_model_ex(
            sphere,
            camera.position,
            rl.Vector3(1, 0, 0),
            -90,
            rl.Vector3(-500, -500, -500),
            rl.WHITE
        )
        rl.draw_model_ex(
            background,
            rl.Vector3(100, -30, -100),
            rl.Vector3(0, 70, 0),
            vis.angle * 2,
            rl.Vector3(0.1, 0.1, 0.1),
            rl.WHITE
        )

        vis.draw_map()
        vis.draw_link()
        vis.draw_moove_ship()
        vis.angle += 0.3
        rl.end_mode_3d()
        if count > 0:
            rl.draw_text(
                f"{count} ships",
                0,
                0,
                20,
                rl.RED
            )

        rl.end_drawing()

    rl.close_window()
