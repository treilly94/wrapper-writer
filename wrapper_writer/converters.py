import re
import string


def lower_camel(name, split_char="_"):
    """Converts a given name into lower camelcase

    :param name: The name to be converted
    :type name: str
    :param split_char: The character that separates words in the name.
    :type split_char: str
    :return: str
    """
    words = name.split(split_char)
    upper = [w.capitalize() for w in words[1:]]
    return words[0] + "".join(upper)


def upper_camel(name, split_char="_"):
    """Converts a given name into upper camel case

    :param name: The name to be converted
    :type name: str
    :param split_char: The character that separates words in the name.
    :type split_char: str
    :return: str
    """
    return "".join(w.capitalize() for w in name.split(split_char))


def underscores(name):
    """Converts a given name from camel case to underscores.

    :param name: The name to be converted
    :type name: str
    :return: str
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class CustomFormatter(string.Formatter):
    """This class extends string.Formatter and adds the functionality to convert to upper or lower camelcase"""

    def convert_field(self, value, conversion):
        if conversion == 'u':
            return upper_camel(value)
        elif conversion == 'l':
            return lower_camel(value)
        else:
            return super().convert_field(value, conversion)
