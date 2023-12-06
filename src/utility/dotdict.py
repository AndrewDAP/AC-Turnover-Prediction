"""
dot.notation access to dictionary attributes
"""


class Dotdict(dict):
    """
    dot.notation access to dictionary attributes

    Example:
        >>> my_dict = {'a': 1, 'b': 2}
        >>> my_dict = dotdict(my_dict)
        >>> my_dict.a
        1
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
