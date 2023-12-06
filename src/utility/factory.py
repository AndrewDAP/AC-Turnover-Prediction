"""
Factory class for creating objects based on a name.
"""

from typing import Dict, Type


class Factory:
    """
    Factory class for creating objects based on a name.

    args:
        registry: A dictionary of name to class. If None, an empty dictionary
            is used.
    """

    def __init__(self, *, registry: Dict[str, Type] = None):
        assert registry is None or isinstance(registry, dict)
        self._registry = registry or {}

    def register(self, name: str, cls: Type):
        """
        Register a class with the factory.

        args:
            name: The name of the class.
            cls: The class to register.
        """
        self._registry[name] = cls

    def create(self, name: str, *args, **kwargs):
        """
        Create an object based on a name.

        args:
            name: The name of the object to create.
            *args: Positional arguments to pass to the constructor.
            **kwargs: Keyword arguments to pass to the constructor.
        """
        if name not in self._registry:
            raise ValueError(f"Unknown {name}")

        return self._registry[name](*args, **kwargs)
