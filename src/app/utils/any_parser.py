from typing import Dict, Type, Callable, TypeVar, Any, Optional


T = TypeVar('T')

class AnyParser():
    _parsers: Dict[Type, Callable[[str], Any]] = {
        str: str,
        int: int,
        float: float,
        bool: lambda x: x.lower() in ['true', 'false']
    }

    @classmethod
    def register_parser(cls, target_type: Type[T], parser: Callable[[str], T]):
        cls._parsers[target_type] = parser

    @classmethod
    def parse(cls, value: str, target_type: Type[T]) -> Optional[T]:
        try:
            return cls._parsers[target_type](value)
        except (ValueError, TypeError, KeyError):
            return None
