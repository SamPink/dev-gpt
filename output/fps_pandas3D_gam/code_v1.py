import sys
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec3, Vec4
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionSphere
from panda3d.core import WindowProperties


class FPSGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable Mouse Control
        self.disable_mouse()

        # Setting up window properties
        window_properties = WindowProperties()
        window_properties.set_size(1280, 720)
        self.win.request_properties(window_properties)

        # Change the camera position
        self.camera.set_pos(0, -20, 2)

        # Load model and texture for the environment
        self.environment_model = self.loader.load_model("models/misc/ground")
        self.environment_model.reparent_to(self.render)
        self.environment_model.set_scale(40, 40, 1)
        self.environment_texture = self.loader.load_texture("models/misc/grid.png")
        self.environment_model.set_texture(self.environment_texture, 1)

        # Load a character
        self.character = Actor("models/player/zombie")
        self.character.reparent_to(self.render)
        self.character.set_pos(0, 15, 0)

        # Add Ambient Light
        ambient_light = AmbientLight("ambientLight")
        ambient_light.set_color(Vec4(0.2, 0.2, 0.2, 1))
        self.ambient_light_node_path = self.render.attach_new_node(ambient_light)
        self.render.set_light(self.ambient_light_node_path)

        # Add Directional Light
        directional_light = DirectionalLight("directionalLight")
        directional_light.set_color(Vec4(0.6, 0.6, 0.6, 1))
        self.directional_light_node_path = self.render.attach_new_node(directional_light)
        self.directional_light_node_path.set_hpr(0, -30, 0)
        self.render.set_light(self.directional_light_node_path)

        # Create a task manager to handle events continuously
        self.task_mgr.add(self.update_task, "update")

        # Create a traverser for collisions
        self.collision_traverser = CollisionTraverser()

        # Create a handler for collisions
        self.collision_handler = CollisionHandlerQueue()

        # Set up a CollisionSphere for the character
        self.character_coll_sphere = CollisionSphere(0, 1, 1, 1)
        self.character_coll_node = CollisionNode("character collision")
        self.character_coll_node.add_solid(self.character_coll_sphere)
        self.character_coll_node_path = self.character.attach_new_node(self.character_coll_node)
        self.character_coll_node.set_from_collide_mask(0x1)
        self.character_coll_node.set_into_collide_mask(0)

        # Add the character collision to the traverser
        self.collision_traverser.add_collider(self.character_coll_node_path, self.collision_handler)

    def update_task(self, task):
        # Check collisions
        self.collision_traverser.traverse(self.render)

        for entries in self.collision_handler.entries:
            # Do some game logic here, e.g., handle character interactions, add points, or change levels

            pass

        return task.cont


game = FPSGame()
game.run()