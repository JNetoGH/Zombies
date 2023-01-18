import math
import numpy.linalg
from pygame import Vector2, Surface
from JNeto_engine_lite import constants
from JNeto_engine_lite.components import Sprite, Collider
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject
from game_object_barrier import Barrier


class Zombie(GameObject):

    def __init__(self, initial_postion: Vector2):
        super().__init__("zombie")

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("res/zombie.png"))
        self.sprite.scale_image(0.4)

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, 35, 35))
        self.collider.collidable_classes.append(Barrier)

        # movement and related
        self.move_speed = 75
        self.angle_to_player = 20
        self.angular_velocity = 100
        self.direction_to_player = Vector2(0, 0)

        # initial position
        self.transform.move_position(initial_postion)

    def update(self):

        # DISTANCE TO PLAYER (used to get the direction to player)
        player_position = self.scene.get_game_object("player").transform.get_position_copy()
        zombie_position = self.transform.get_position_copy()
        distance_to_player = player_position - self.transform.get_position_copy()

        # DIRECTION TO PLAYER (normalizes the dir, avoiding div by 0 exeptions, ex: vector=(0, 0))
        self.direction_to_player = distance_to_player
        if numpy.linalg.norm(distance_to_player) > 0:
            self.direction_to_player = self.direction_to_player / numpy.linalg.norm(self.direction_to_player)

        # MOVEMENT (do not transpass barries)
        new_position = zombie_position + self.direction_to_player * self.move_speed * GameLoop.Delta_Time
        self.transform.move_position(new_position)

        # ANGLE (used for rotation, atan2 is used to get the angle between two points)
        up_direction = Vector2(0, 0)
        dx = up_direction.x - self.direction_to_player.x
        dy = up_direction.y - self.direction_to_player.y
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        # converts radians to degrees
        self.angle_to_player = (rads * 180/math.pi) + 90  # +90º because the img faces ↑, so the default → turns ↑

        # KEEPS THE ANGLE IN 0º <=> 360º RANGE (in order to work with my cached texts for perfromance)
        self.angle_to_player = constants.get_converted_angle_to_0_360_range(self.angle_to_player)

        # ROTATION
        self.sprite.rotate_image(self.angle_to_player)

    def render_gizmos(self, game_surface: Surface):
        # distance to player
        constants.draw_special_gizmos(game_surface, self.transform.get_position_copy(), self.direction_to_player, self.angle_to_player)

    def destroy(self):
        self.scene.remove_game_object(self)
