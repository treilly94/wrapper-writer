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
