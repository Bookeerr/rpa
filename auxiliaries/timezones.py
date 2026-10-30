"""Zona horaria en CPython y runtime congelado de Rocketbot sin zoneinfo."""
try:
    from zoneinfo import ZoneInfo
except ModuleNotFoundError:
    from pytz import timezone as ZoneInfo
