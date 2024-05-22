"""Utility functions, to be used across the entire project.

Following a suggestion from Two Scoops of Django 1.8.
"""


def in_to_cm(inches: float) -> float:
    return inches / 2.54


def cm_to_in(centimeters: float) -> float:
    return centimeters * 2.54


def g_to_oz(grams: float) -> float:
    return grams / 28.35


def oz_to_g(ounces: float) -> float:
    return ounces * 28.35
