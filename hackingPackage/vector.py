"""
This module provides a Vec3 class with common functionalities such as:  \n
> addition of vectors (v1 + v2)                                         \n
> subtraction of vectors (v1 - v2)                                      \n
> dot product of two vectors (v1 * v2)                                  \n
> scaling of a vector where s is a float (v * s | s * v)                \n
> length of the vector (abs(v))                                         \n
-----------------------------------                                     \n
Further functionalities include:                                        \n
> v.load() returns a list [v.x, v.y, v.z]                               \n
> v.validate_view_angles() makes pitch yaw and roll valid for csgo      \n
"""

from math import sqrt


class Vec3:
    def __init__(self, *args):
        if type(args[0]) == list or type(args[0]) == tuple:
            args = args[0]
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return self.__class__(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return self.__class__(x, y, z)

    def __mul__(self, other):
        if type(self) == type(other) == Vec3:
            return self.x * other.x + self.y * other.y + self.z * other.z
        elif (type(other) == float or type(other) == int) and type(self) == Vec3:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return "[x, y, z] = " + str([self.x, self.y, self.z])

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def load(self):
        return [self.x, self.y, self.z]

    def validate_view_angles(self):
        if self.x > 89:
            self.x = 89
        elif self.x < -89:
            self.x = -89

        while self.y > 180:
            self.y -= 360
        while self.y <= -180:
            self.y += 360

        self.z = 0
        return self.__class__(self.x, self.y, self.z)
