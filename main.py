from math import *
import numpy as np
from time import sleep

WHEEL_RADIUS = 2.95
CENTER_TO_WHEEL = 7
STEP = 0.1


def calculate_velocity_from_powers(wheel_1_angular_velocity,
                                   wheel_2_angular_velocity,
                                   wheel_3_angular_velocity,
                                   wheel_4_angular_velocity):

    velocity_x = (wheel_1_angular_velocity +
                  wheel_2_angular_velocity +
                  wheel_3_angular_velocity +
                  wheel_4_angular_velocity) * (WHEEL_RADIUS / 4)

    velocity_y = (-wheel_1_angular_velocity +
                  wheel_2_angular_velocity +
                  wheel_3_angular_velocity +
                  -wheel_4_angular_velocity) * (WHEEL_RADIUS / 4)

    angular_velocity = (-wheel_1_angular_velocity +
                        wheel_2_angular_velocity +
                        -wheel_3_angular_velocity +
                        wheel_4_angular_velocity) * (WHEEL_RADIUS / (8 * CENTER_TO_WHEEL))

    return [velocity_x, velocity_y, angular_velocity]


def calculate_powers_from_velocity(velocity_x, velocity_y, velocity_angular):
    reciprocal_radius = 1 / WHEEL_RADIUS
    wheel_1_angular_velocity = reciprocal_radius * (velocity_x - velocity_y - (velocity_angular * (2 * CENTER_TO_WHEEL)))
    wheel_2_angular_velocity = reciprocal_radius * (velocity_x + velocity_y + (velocity_angular * (2 * CENTER_TO_WHEEL)))
    wheel_3_angular_velocity = reciprocal_radius * (velocity_x + velocity_y - (velocity_angular * (2 * CENTER_TO_WHEEL)))
    wheel_4_angular_velocity = reciprocal_radius * (velocity_x - velocity_y + (velocity_angular * (2 * CENTER_TO_WHEEL)))
    vel = np.array([wheel_1_angular_velocity, wheel_2_angular_velocity, wheel_3_angular_velocity, wheel_4_angular_velocity])
    return vel


def move_steps(pos, p1, p2, p3, p4, n, should_print):
    for _ in range(n):
        velocity = calculate_velocity_from_powers(p1, p2, p3, p4)
        a = pos[2]
        vx = velocity[0]
        vy = velocity[1]
        da = velocity[2]
        a += da

        real_vx = (vx * cos(a)) - (vy * sin(a))
        real_vy = (vy * cos(a)) + (vx * sin(a))

        pos = np.add(pos, [real_vx, real_vy, 0])
        pos[2] = a

    if should_print:
        print_info(pos)
    return pos


def print_info(pos):
    print('The robot is at '+str(pos[0:2])+' and facing an angle of '+str(degrees(pos[2]))+' degrees.')


robot_pos = [0, 0, 0]

robot_pos = move_steps(robot_pos, -0.01, 0.01, -0.01, 0.01, 50, True)
