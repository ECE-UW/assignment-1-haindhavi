import re


class CommandParserException(Exception):
    pass


def parse(line):
    line = line.strip()
    m = re.match("^([acrg])([ ]+.*)?", line)
    command, rest = m.groups()

    if command == "g":
        if rest is not None:
            raise CommandParserException("Invalid Input. Usage: g")
        return {"command": "GENERATE_GRAPH"}

    if command == "r":
        try:
            street_name, rest = get_street_name(rest)
            if rest is not None:
                raise
        except:
            raise CommandParserException('Invalid Input. Usage: r "street_name"')

        return {"command": "REMOVE_STREET", "street_name": street_name}

    if command == "a":
        try:
            street_name, rest = get_street_name(rest)
            coordinates, rest = get_coordinates(rest)
            if rest is not None:
                raise
        except:
            raise CommandParserException(
                'Invalid Input. Usage: a "street_name" (x1,y1) (x2,y2) ... '
            )

        return {
            "command": "ADD_STREET",
            "street_name": street_name,
            "coordinates": coordinates,
        }

    if command == "c":
        try:
            street_name, rest = get_street_name(rest)
            coordinates, rest = get_coordinates(rest)
            if rest is not None:
                raise
        except:
            raise CommandParserException(
                'Invalid Input. Usage: a "street_name" (x1,y1) (x2,y2) ... '
            )

        return {
            "command": "CHANGE_STREET",
            "street_name": street_name,
            "coordinates": coordinates,
        }

    raise CommandParserException("Input Invalid. Usage: (a|t|g|c) ...")


def get_street_name(line):
    line = line.strip()
    m = re.match('^"([\w ]+)"( .*)?', line)
    street_name, rest = m.groups()
    return street_name, rest


def get_coordinates(line):
    line += " "
    m = re.match("^\s*(\([ ]*([-\d]+)[ ]*,[ ]*([-\d]+)[ ]*\)[ ]+)+$", line)
    if m is None:
        raise
    coordinates = re.findall("\([ ]*([-\d]+)[ ]*,[ ]*([-\d]+)[ ]*\)[ ]+", line)
    coordinates = [(int(a), int(b)) for (a, b) in coordinates]
    return coordinates, None


# tests

# parse("a \"Weber Street\" (1,-3) (2,4) (3,8)")
# parse("r \"Bentley's Street\" (1,-3) (2,4) (3,8)")
# parse("g")
# parse("c \"Darwin Street\" (1,-3) (-3,-8)")
