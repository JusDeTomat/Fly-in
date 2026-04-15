from enum import Enum


class Cost(Enum):
    PRIORITY = 1.0
    NORMAL = 1.0
    RESTRICTED = 2.0


class Model(Enum):
    BLACK_HOLE = 'src/visual/source/black_hole.glb'
    START = 'src/visual/source/start.glb'
    SHIP = 'src/visual/source/spaceship.glb'
    NEPTUNE = 'src/visual/source/neptune.glb'
    SATURN = 'src/visual/source/saturn.glb'
    MOON = 'src/visual/source/moon.glb'
    SUN = 'src/visual/source/sun.glb'
    END = 'src/visual/source/end.glb'
    SKYBOX = 'src/visual/source/skybox.jpg'
