from math import radians, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec3, Vec4
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionSphere
from panda3d.core import WindowProperties, MouseButton


class FPSGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Variables to store the speeds of camera movement and rotation
        self.movement_speed = 0.1
        self.rotation_speed = 1.0
        self.hpr = self.camera.get_hpr()
        self.movement_direction = Vec3(0, 0, 0)  # Initialize movement_direction

        # ... (Disable Mouse Control, Setting up window properties, Load environment and character, etc.)

        # Accept keyboard and mouse events
        self.accept("w", self.set_movement_direction, [Vec3(0, 1, 0)])
        self.accept("s", self.set_movement_direction, [Vec3(0, -1, 0)])
        self.accept("a", self.set_movement_direction, [Vec3(-1, 0, 0)])
        self.accept("d", self.set_movement_direction, [Vec3(1, 0, 0)])
        self.accept("w-up", self.set_movement_direction, [Vec3(0, 0, 0)])
        self.accept("s-up", self.set_movement_direction, [Vec3(0, 0, 0)])
        self.accept("a-up", self.set_movement_direction, [Vec3(0, 0, 0)])
        self.accept("d-up", self.set_movement_direction, [Vec3(0, 0, 0)])
        self.accept("mouse1", self.rotate_camera)

        # Create a task manager to handle events continuously
        self.task_mgr.add(self.update_task, "update")

    def set_movement_direction(self, direction):
        self.movement_direction = direction

    def move_camera(self):
        self.camera.set_pos(self.camera.get_pos() + self.movement_direction * self.movement_speed)

    def rotate_camera(self):
        if self.mouseWatcherNode.has_mouse():
            dx = self.mouseWatcherNode.get_mouse_x() * self.rotation_speed
            dy = self.mouseWatcherNode.get_mouse_y() * self.rotation_speed

            self.hpr += Vec3(dy, 0, -dx)
            self.camera.set_hpr(self.hpr)

    def update_task(self, task):
        # Move and rotate the camera
        self.move_camera()
        self.rotate_camera()

        # ... (Check collisions and game logic as before)

        return task.cont


game = FPSGame()
game.run()