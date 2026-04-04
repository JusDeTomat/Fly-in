import pyray as rl
import backend.parcing as par
import math

class Ship:
    def __init__(self,id):
        self.ship_id = id
        self.id_path = 1
        self.t = 0.005
        self.model = rl.load_model('source/spaceship.glb')
        self.position = rl.Vector3(0, 1.5 + 0.4 * self.ship_id, 0)
        self.angle = 0
        self.end = False


class Visual:
    def __init__(self, dico_info):

        self.dico_info = dico_info
        self.path = [[(0, 0), (1, 0), (1, 1), (2, 1), (6, 0), (6, -1), (12, -2), (13, -2), (14, -2), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0)]]* 25
        print(self.path)
        self.angle = 0
        self.level_ves = 0
        self.lst_ship = []
        self.add_ship()
        self.speed = 0.005
        self.stop = True
    
    def add_ship(self):
        for i in range(self.dico_info['nb_drones']):
            self.lst_ship.append(Ship(i))

    def draw_map(self):
        x = int(self.dico_info["start"]["x"])
        y = int(self.dico_info["start"]["y"])
        rl.draw_model_ex(
                        start,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.5, 0.5, 0.5),
                        rl.WHITE
                    )
        x = int(self.dico_info["end"]["x"])
        y = int(self.dico_info["end"]["y"])
        rl.draw_model_ex(
                        model,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.01, 0.01, 0.01),
                        rl.WHITE
                    )
        key_hub = dico["hub"].keys()
        for element in key_hub:
            x = int(self.dico_info["hub"][element]["x"])
            y = int(self.dico_info["hub"][element]["y"])
            mode = self.dico_info["hub"][element].get("zone", "normal")
            color = self.dico_info['hub'][element].get('color', 'WHITE').upper()
            rl.draw_sphere(rl.Vector3(x * 3, 1, y * 3), 0.3, rl.WHITE)
            if (mode == "restricted"):
                rl.draw_model_ex(
                        model,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.01, 0.01, 0.01),
                        rl.WHITE
                    )
            elif (mode == "blocked"):
                rl.draw_model_ex(
                        model4,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.05, 0.05, 0.05),
                        rl.WHITE
                    )
            elif (mode == "priority"):
                rl.draw_model_ex(
                        model3,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.01, 0.01, 0.01),
                        rl.WHITE
                    )
            elif element != self.dico_info["start"]["name"] and element != self.dico_info["end"]["name"]:
                rl.draw_model_ex(
                        model2,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 20),
                        self.angle,
                        rl.Vector3(0.001, 0.001, 0.001),
                        rl.WHITE
                    )

    def draw_link(self):
        link = self.dico_info["link"]
        
        for element in link:
            x1 = int(self.dico_info["hub"][element['hub1']]["x"])
            y1 = int(self.dico_info["hub"][element['hub1']]["y"])
            x2 = int(self.dico_info["hub"][element['hub2']]["x"])
            y2 = int(self.dico_info["hub"][element['hub2']]["y"])
            rl.draw_line_3d(rl.Vector3(x1 * 3, 0, y1 * 3), rl.Vector3(x2 * 3, 0, y2 * 3), rl.WHITE)
    
    def draw_moove_ship(self):
        stop = 0
        end = 0
        for ship in self.lst_ship:
            # print(ship.ship_id, self.stop, ship.t)
            if self.stop or ship.end:
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
                        end = 1
        if end:
            self.end = True
        if stop:
            self.stop = True




rl.init_window(1800, 1000, "Fly-In")


camera = rl.Camera3D(
    rl.Vector3(0.0, 2.0, 6.0),
    rl.Vector3(0.0, 1.0, 0.0),
    rl.Vector3(0.0, 1.0, 0.0),
    60.0,
    rl.CAMERA_PERSPECTIVE
)

rl.set_target_fps(60)
dico = par.read_file("backend/test.txt")
vis = Visual(dico)
background = rl.load_model('source/black_hole.glb')
start = rl.load_model("source/earth.glb")
model = rl.load_model("source/neptune.glb")
model2 = rl.load_model('source/saturn.glb')
model3 = rl.load_model('source/moon.glb')
model4 = rl.load_model('source/sun.glb')
light = rl.load_model('source/light.glb')
image = rl.load_image("source/skybox.jpg")
texture = rl.load_texture("source/skybox.jpg")
shader = rl.load_shader("skybox.vs", "skybox.fs")
cubemap = rl.load_texture_cubemap(image, rl.CUBEMAP_LAYOUT_AUTO_DETECT)
mesh = rl.gen_mesh_sphere(1.0, 32, 100)
sphere = rl.load_model_from_mesh(mesh)
sphere.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture

while not rl.window_should_close():
    if rl.is_mouse_button_down(rl.MOUSE_LEFT_BUTTON) or rl.is_mouse_button_down(rl.MOUSE_RIGHT_BUTTON):
        rl.update_camera(camera, rl.CAMERA_FREE)
    else:
        if rl.is_key_pressed(rl.GLFW_KEY_SPACE):
            if vis.stop:
                vis.stop = False
    if rl.is_key_down(rl.KEY_UP):
        vis.speed += 0.005
    if rl.is_key_down(rl.KEY_DOWN):
        vis.speed -= 0.005
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    rl.begin_mode_3d(camera)
    rl.draw_model_ex(
                     sphere, 
                     rl.Vector3(0, 0, 0), 
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
    rl.end_drawing()

rl.close_window()
print