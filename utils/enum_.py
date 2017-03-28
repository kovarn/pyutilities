from enum import Enum


class AutoName(str, Enum):
    """
    A str enumeration, where enum values are equal to enum names.
    Useful as substitution for str constants, especially in
    pandas DataFrame column names.
    """

    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.name
