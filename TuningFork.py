#!/usr/bin/env python3

# Copyright 2016 Corey Clayton <can.of.tuna@gmail.com>

from math import pi, sqrt
from abc import ABC, abstractmethod
from enum import Enum

class Steel(Enum):
    y_modulus = 200 * 1000 * 1000 * 1000 # 200 GPa
    rho = 7850 # in kg/m^3

class Aluminum(Enum):
    y_modulus = 69 * 1000 * 1000 * 1000 # 69 GPa
    rho = 2712 # in kg/m^3

class Brass(Enum):
    y_modulus = 112.5 * 1000 * 1000 * 1000 # 112 GPa
    rho = 8520 # in kg/m^3

class Lead(Enum):
    y_modulus = 13.789 * 1000 * 1000 * 1000 # 13.8 GPa
    rho = 11340 # in kg/m^3

class Concrete(Enum):
    y_modulus = 17 * 1000 * 1000 * 1000 # 17 GPa
    rho = 2400

    
class Tine(ABC):
    """
    This class represents the part of a tuning fork that vibrates.

    Tine is an abstract base class since the math for differently shaped
    tines will be different. 
    """
    @abstractmethod
    def second_moment_area():
        pass

    @abstractmethod
    def cross_sectional_area():
        pass
    
class RectangularTine(Tine):
    """
    Rectangular Tine: Has a width and a height
    """
    width = 0
    height = 0
    material = None

    def __init__(self, width, height, material = Steel):
        self.width = width
        self.height = height
        self.material = material

    def second_moment_area(self):
        """
        Calculate the 2nd moment of inertia

        returns a tuple (Ix, Iy) where Ix and Iy are the 2nd moment of area
        with respect to the x and y axes.
        """
        Ix = (1/12) * self.width * (self.height ** 3)
        Iy = (1/12) * (self.width ** 3) * self.height
        return (Ix, Iy)

    def cross_sectional_area(self):
        return self.width * self.height
    
class CylindricalTine(Tine):
    """
    Cylindrical Tine: the cross section of this tine can be described by a radius, r
    """
    radius = 0
    material = None

    def __init__(self, r, material = Steel):
        self.radius = r
        self.material = material

    def second_moment_area(self):
        """
        Calculate the 2nd moment of inertia

        returns a tuple (Ix, Iy) where Ix and Iy are the 2nd moment of area
        with respect to the x and y axes.
        """
        Ix = (pi/4) * (self.radius ** 4)
        Iy = (pi/4) * (self.radius ** 4)
        return (Ix, Iy)

    def cross_sectional_area(self):
        return pi * (self.radius ** 2)
    
def calc_fork_len(freq, in_tine):
    """
    This function calculates the length of tines (prongs) required for
    a the given tuning fork properties and frequency

    Inputs:

    - freq - The frequency in Hz

    - in_tine - An object of the Tine class defining the properties of 
                the desired fork
    

    ** Note **

    This calculation is done using only the x component of the 2nd moment 
    of inertia. This is based on the formula on wikipedia (as of Dec 2016).
    I was not able to find any additional references on the matter but it
    seems that the vibration in x is primarily what we care about. The x 
    axis is the parallel to the width in rectangular tines.
    """
    k = (1.875104068711 ** 2) / (2 * pi)
    L_squared = (k / freq) * sqrt(
                                   (in_tine.material.y_modulus.value * in_tine.second_moment_area()[0]) /
                                   (in_tine.material.rho.value * in_tine.cross_sectional_area())
                                  )
    return sqrt(L_squared)
    

def in2mm(inches):
    return inches * 25.4

def mm2in(mm):
    return mm/25.4

def in2m(inches):
    return in2mm(inches) / 1000

def m2in(m):
    return mm2in(m*1000)


