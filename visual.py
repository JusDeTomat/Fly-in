import pyray as rl

class Ship:
    def __init__(self, model):
        self.model = model
        self.position = rl.Vector3(0, 2, 0)
        self.end = False


class Visual:
    def __init__(self):
        self.map = [
            [0,0,1,1,2,0],
            [2,0,0,3,0,1]
            ]
        self.link = [
            ((2, 0), (0, 1)),
            ((0, 1), (5, 1))
        ]
        self.path = [
            ((2, 0), (0, 1)),
            ((0, 1), (5, 1))
        ]
        self.angle = 0
        self.level_ves = 0
        self.ship = Ship(rl.load_model('source/space_fighter_the_protector_of_the_galaxy.glb'))
        self.id_path = 0
        self.t = 0.005

    def draw_map(self):
        x = 0
        y = 0
        for line in self.map:
            for element in line:
                if element == 1:
                    rl.draw_model_ex(
                            model,
                            rl.Vector3(x, 0, y),
                            rl.Vector3(x, 90, y),
                            self.angle,
                            rl.Vector3(0.01, 0.01, 0.01),
                            rl.WHITE
                        )
                if element == 2:
                    rl.draw_model_ex(
                            model2,
                            rl.Vector3(x, 0, y),
                            rl.Vector3(x, 90, y),
                            self.angle,
                            rl.Vector3(0.001, 0.001, 0.001),
                            rl.WHITE
                        )
                if element == 3:
                        rl.draw_model_ex(
                            model3,
                            rl.Vector3(x, 0, y),
                            rl.Vector3(x, 90, y),
                            self.angle,
                            rl.Vector3(0.2, 0.2, 0.2),
                            rl.WHITE
                        )
                x += 3
            x = 0
            y += 3

    def draw_link(self):
        for link in self.link:
            x1,y1 = link[0]
            x2,y2 = link[1]
            rl.draw_line_3d(rl.Vector3(x1 * 3, 0, y1 * 3), rl.Vector3(x2 * 3, 0, y2 * 3), rl.WHITE)
    
    def draw_moove_ship(self):
        if self.ship.end:
            return
        x1, y1 = self.path[self.id_path][0]
        x2, y2 = self.path[self.id_path][1]
        self.ship.position.x = x1 * 3 + (x2 * 3 - x1 * 3) * self.t
        self.ship.position.z = y1 * 3 + (y2 * 3 - y1 * 3) * self.t
        rl.draw_model(self.ship.model, self.ship.position, 0.005, rl.WHITE)
        self.t += 0.005
        if (self.t >= 1):
            self.t = 0.005
            if (self.id_path + 1 <= len(self.path) - 1):
                self.id_path += 1
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
model = rl.load_model("source/mercury_planet_brass_stylised.glb")
model2 = rl.load_model('source/saturn.glb')
model3 = rl.load_model('source/moon.glb')
light = rl.load_model('source/light.glb')


while not rl.window_should_close():
    if rl.is_mouse_button_down(rl.MOUSE_LEFT_BUTTON) or rl.is_mouse_button_down(rl.MOUSE_RIGHT_BUTTON):
        rl.update_camera(camera, rl.CAMERA_FREE)
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    rl.begin_mode_3d(camera)

    rl.draw_model_ex(
                    background,
                    rl.Vector3(100, -30, -100),
                    rl.Vector3(0, 70, 0),
                    vis.angle / 2,
                    rl.Vector3(0.1, 0.1, 0.1),
                    rl.WHITE
                )
    rl.draw_sphere(rl.Vector3(95, -28, -95), 15, rl.LIGHTGRAY)
    vis.draw_map()
    vis.draw_link()
    vis.draw_moove_ship()
    vis.draw_moove_ship()
    vis.angle += 0.3
    # rl.draw_sphere(rl.Vector3(0, 1.5, 0), 0.3, rl.RED)
    # rl.draw_model(model, rl.Vector3(0, 0, 0), 0.2, rl.WHITE)
    # rl.draw_model(model2, rl.Vector3(3, 0, 0), 0.7, rl.WHITE)
    # rl.draw_line_3d(rl.Vector3(0, 0, 0), rl.Vector3(3, 0, 0), rl.WHITE)

    rl.end_mode_3d()
    rl.end_drawing()

rl.close_window()
