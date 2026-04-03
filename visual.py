import pyray as rl
import backend.parcing as par
import math

class Ship:
    def __init__(self, model):
        self.model = model
        self.position = rl.Vector3(0, 1.5, 0)
        self.angle = 0
        self.end = False


class Visual:
    def __init__(self):

        self.path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (11, 1), (11, -1), (12, 2), (13, 2), (14, 2), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0)]
        self.angle = 0
        self.level_ves = 0
        self.ship = Ship(rl.load_model('source/spaceship.glb'))
        self.id_path = 1
        self.t = 0.005
        self.speed = 0.005
        self.stop = True

    def draw_map(self, dico_info):
        x = int(dico_info["start"]["x"])
        y = int(dico_info["start"]["y"])
        rl.draw_model_ex(
                        start,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 0),
                        self.angle,
                        rl.Vector3(0.5, 0.5, 0.5),
                        rl.WHITE
                    )
        x = int(dico_info["end"]["x"])
        y = int(dico_info["end"]["y"])
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
            x = int(dico_info["hub"][element]["x"])
            y = int(dico_info["hub"][element]["y"])
            mode = dico_info["hub"][element].get("zone", "normal")
            color = dico_info['hub'][element].get('color', 'WHITE').upper()
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
            elif element != dico_info["start"]["name"] and element != dico_info["end"]["name"]:
                rl.draw_model_ex(
                        model2,
                        rl.Vector3(x * 3, 0, y * 3),
                        rl.Vector3(0, 90, 20),
                        self.angle,
                        rl.Vector3(0.001, 0.001, 0.001),
                        rl.WHITE
                    )

    def draw_link(self, dico_info):
        link = dico_info["link"]
        
        for element in link:
            x1 = int(dico_info["hub"][element['hub1']]["x"])
            y1 = int(dico_info["hub"][element['hub1']]["y"])
            x2 = int(dico_info["hub"][element['hub2']]["x"])
            y2 = int(dico_info["hub"][element['hub2']]["y"])
            rl.draw_line_3d(rl.Vector3(x1 * 3, 0, y1 * 3), rl.Vector3(x2 * 3, 0, y2 * 3), rl.WHITE)
    
    def draw_moove_ship(self):
        if self.stop or self.ship.end:
            rl.draw_model_ex(
                        self.ship.model,
                        self.ship.position,
                        rl.Vector3(0, 1, 0),
                        self.ship.angle,
                        rl.Vector3(0.05, 0.05, 0.05),
                        rl.WHITE
                    )
            return
        x1, y1 = self.path[self.id_path - 1]
        x2, y2 = self.path[self.id_path]
        self.ship.position.x = x1 * 3 + (x2 * 3 - x1 * 3) * self.t
        self.ship.position.z = y1 * 3 + (y2 * 3 - y1 * 3) * self.t
        direction = rl.Vector3(
            x2 * 3 - self.ship.position.x,
            0,
            y2 * 3 - self.ship.position.z
        )
        direction = rl.vector3_normalize(direction)
        self.ship.angle = math.degrees(math.atan2(direction.x, direction.z))
        rl.draw_model_ex(
                        self.ship.model,
                        self.ship.position,
                        rl.Vector3(0, 1, 0),
                        self.ship.angle,
                        rl.Vector3(0.05, 0.05, 0.05),
                        rl.WHITE
                    )
        self.t += self.speed
        if (self.t >= 1):
            self.t = 0.005
            if (self.id_path + 1 <= len(self.path) - 1):
                self.id_path += 1
                self.stop = True
            else:
                self.ship.end = True




rl.init_window(1800, 1000, "Fly-In")


camera = rl.Camera3D(
    rl.Vector3(0.0, 2.0, 6.0),
    rl.Vector3(0.0, 1.0, 0.0),
    rl.Vector3(0.0, 1.0, 0.0),
    60.0,
    rl.CAMERA_PERSPECTIVE
)

rl.set_target_fps(60)
vis = Visual()
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

dico = par.read_file("backend/test.txt")
print(dico)

while not rl.window_should_close():
    if rl.is_mouse_button_down(rl.MOUSE_LEFT_BUTTON) or rl.is_mouse_button_down(rl.MOUSE_RIGHT_BUTTON):
        rl.update_camera(camera, rl.CAMERA_FREE)
    else:
        if rl.is_key_pressed(rl.GLFW_KEY_SPACE):
            if vis.stop:
                vis.stop = False
            else:
                vis.stop = True
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
    vis.draw_map(dico)
    vis.draw_link(dico)
    vis.draw_moove_ship()
    vis.angle += 0.3

    rl.end_mode_3d()
    rl.end_drawing()

rl.close_window()
print