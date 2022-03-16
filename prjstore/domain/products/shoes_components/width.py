from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Width:
    name: str
    short_name: str
    width_of_insole: Optional[float] = None
