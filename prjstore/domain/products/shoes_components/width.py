from contracts import contract
from pydantic.dataclasses import dataclass


@dataclass
class Width:
    """
>>> width = Width(name='Wide', short_name='EE')
>>> width.name
'Wide'
>>> width.short_name
'EE'
    """
    name: str
    short_name: str

