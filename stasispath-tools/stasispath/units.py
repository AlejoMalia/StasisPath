"""
Unit conversions, physical dimensionality checks, and validation functions.
"""

from typing import Union

# Absolute zero in Celsius
T_ZERO_ABS_C: float = -273.15


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin."""
    if celsius < T_ZERO_ABS_C:
        raise ValueError(f"Temperature {celsius} °C is below absolute zero (-273.15 °C).")
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    if kelvin < 0:
        raise ValueError(f"Temperature {kelvin} K cannot be negative.")
    return kelvin - 273.15


def hours_to_minutes(hours: float) -> float:
    """Convert hours to minutes."""
    if hours < 0:
        raise ValueError("Time duration cannot be negative.")
    return hours * 60.0


def minutes_to_hours(minutes: float) -> float:
    """Convert minutes to hours."""
    if minutes < 0:
        raise ValueError("Time duration cannot be negative.")
    return minutes / 60.0


def seconds_to_hours(seconds: float) -> float:
    """Convert seconds to hours."""
    if seconds < 0:
        raise ValueError("Time duration cannot be negative.")
    return seconds / 3600.0


def ml_to_liters(ml: float) -> float:
    """Convert milliliters (cm³) to liters."""
    if ml < 0:
        raise ValueError("Volume cannot be negative.")
    return ml / 1000.0


def liters_to_ml(liters: float) -> float:
    """Convert liters to milliliters (cm³)."""
    if liters < 0:
        raise ValueError("Volume cannot be negative.")
    return liters * 1000.0


def k_per_sec_to_c_per_min(k_per_s: float) -> float:
    """Convert cooling/warming rate from K/s (or °C/s) to °C/min."""
    return k_per_s * 60.0


def c_per_min_to_k_per_sec(c_per_min: float) -> float:
    """Convert cooling/warming rate from °C/min to K/s (or °C/s)."""
    return c_per_min / 60.0


def validate_positive(value: float, name: str) -> None:
    """Assert that a parameter is strictly positive."""
    if value <= 0:
        raise ValueError(f"{name} must be strictly positive (> 0), got: {value}")


def validate_non_negative(value: float, name: str) -> None:
    """Assert that a parameter is non-negative (>= 0)."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative (>= 0), got: {value}")
