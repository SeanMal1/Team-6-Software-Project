from pygame import Vector2

# Screen
ScreenWidth = 1280
ScreenHeight = 720
TileSize = 16
Scale = 3

OverlayPos = {
    'tool' : (ScreenWidth - 90, ScreenHeight - 90),
    'seed' : (ScreenWidth - 150, ScreenHeight - 40)
}

# Layers at which each entity is rendered, gives 3D effect.
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
}

PlumPos = {
    'Small' : [(18,17),(30,37),(12,50),(30,45),(20,30), (30,10)],
    'Large' : [(10,8), (14,23)]
}

PlayerToolOffset = {
    'left' : Vector2(-17,13),
    'right' : Vector2(17,13),
    'up' : Vector2(0,-3),
    'down' : Vector2(0,17)
}