from dataclasses import dataclass


@dataclass
class Person:
    name: str
    is_victim: bool = False
