import sys
import math
from panda3d.core import Vec3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from pandac.PandaModules import CollisionTraverser, CollisionNode, CollisionSphere, CollisionHandlerEvent


class SimpleDrivingGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.car_speed = 20.0

        self.car = loader.loadModel("models/cartoon_car")  # Replace with the model that you want to use
        self.car.reparentTo(render)
        self.car.setScale(0.07)
        self.car.setPos(0, 0, 0)

        self.camera.setPos(0, -25, 10)
        self.camera.setHpr(0, -15, 0)

        self.taskMgr.add(self.movement_task, "MovementTask")

        self.accept("escape", sys.exit)
        self.accept("arrow_up", self.set_speed, [self.car_speed])
        self.accept("arrow_up-up", self.set_speed, [0])
        self.accept("arrow_down", self.set_speed, [-self.car_speed])
        self.accept("arrow_down-up", self.set_speed, [0])
        self.accept("arrow_left", self.turn_car, [20])
        self.accept("arrow_left-up", self.turn_car, [0])
        self.accept("arrow_right", self.turn_car, [-20])
        self.accept("arrow_right-up", self.turn_car, [0])

    def set_speed(self, speed):
        self.car_speed = speed

    def turn_car(self, delta_angle):
        self.car.setH(self.car.getH() + delta_angle)

    def movement_task(self, task):
        dt = globalClock.getDt()
        dist = self.car_speed * dt

        car_delta = Vec3(math.sin(math.radians(self.car.getH())) * dist, math.cos(math.radians(self.car.getH())) * dist, 0)

        self.camera.setPos(self.camera.getPos() + car_delta)
        self.car.setPos(self.car.getPos() + car_delta)

        return Task.cont


if __name__ == "__main__":
    game = SimpleDrivingGame()
    game.run()