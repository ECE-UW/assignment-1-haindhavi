import re


class CommandParserException(Exception):
    pass


def parse(line):
    line = line.strip()
    m = re.match("^([acrg])( .*)?", line)
    command, rest = m.groups()

    if command == "g":
        return {
            "command": "GENERATE_GRAPH"
        }

    if command == "r":
        street_name, rest = get_street_name(rest)
        return {
            "command": "REMOVE_STREET",
            "street_name": street_name
        }

    if command == "a":
        street_name, rest = get_street_name(rest)
        coordinates, rest = get_coordinates(rest)
        return {
            "command": "ADD_STREET",
            "street_name": street_name,
            "coordinates": coordinates,
        }

    if command == "c":
        street_name, rest = get_street_name(rest)
        coordinates, rest = get_coordinates(rest)
        return {
            "command": "CHANGE_STREET",
            "street_name": street_name,
            "coordinates": coordinates,
        }

    raise CommandParserException()


def get_street_name(line):
    line = line.strip()
    m = re.match('^"([\w\' ?_\-\&\/]+)"( .*)?', line)
    street_name, rest = m.groups()
    return street_name, rest


def get_coordinates(line):
    line = line.strip()
    coordinates = re.findall("\(([-\d]+),([-\d]+)\)", line)
    coordinates = [(int(a), int(b)) for (a, b) in coordinates]
    return coordinates, ""


# tests

# parse("a \"Weber Street\" (1,-3) (2,4) (3,8)")
# parse("r \"Bentley's Street\" (1,-3) (2,4) (3,8)")
# parse("g")
# parse("c \"Darwin Street\" (1,-3) (-3,-8)")
