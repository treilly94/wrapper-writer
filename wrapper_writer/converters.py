def lower_camel(name, split_char="_"):
    words = name.split(split_char)
    upper = [w.capitalize() for w in words[1:]]
    return words[0] + "".join(upper)


def upper_camel(name, split_char="_"):
    return "".join(w.capitalize() for w in name.split(split_char))
