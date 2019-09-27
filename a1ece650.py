#! /usr/bin/python2

import sys

from command_parser import parse, CommandParserException
from street_database import (
    StreetDatabase,
    StreetLookupException,
    InvalidStreetException,
)
from street_graph import StreetGraph


def logerr(msg):
    sys.stderr.write("Error: {}\n".format(msg))


def main():
    db = StreetDatabase()
    while True:
        line = sys.stdin.readline()
        if line == "" or line == None:
            break

        try:
            p = parse(line)

            if p["command"] == "ADD_STREET":
                db.add_street(p["street_name"], p["coordinates"])
                # db.print_db()

            if p["command"] == "CHANGE_STREET":
                db.change_street(p["street_name"], p["coordinates"])
                # db.print_db()

            if p["command"] == "REMOVE_STREET":
                db.delete_street(p["street_name"])
                # db.print_db()

            if p["command"] == "GENERATE_GRAPH":
                graph = StreetGraph(db)
                graph.print_graph()

        except (
            CommandParserException,
            StreetLookupException,
            InvalidStreetException,
        ) as e:
            logerr(e.message)

    sys.exit(0)


if __name__ == "__main__":
    main()
