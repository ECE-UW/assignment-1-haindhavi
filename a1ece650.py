#! /usr/bin/python2

import sys

from command_parser import parse
from street_database import StreetDatabase
from street_graph import StreetGraph


def main():
    db = StreetDatabase()
    while True:
        line = sys.stdin.readline()
        if line == "" or line == None:
            break

        try:
            p = parse(line)
            print (p)

            if p["command"] == "ADD_STREET":
                db.add_street(p["street_name"], p["coordinates"])
                db.print_db()

            if p["command"] == "CHANGE_STREET":
                db.change_street(p["street_name"], p["coordinates"])
                db.print_db()

            if p["command"] == "REMOVE_STREET":
                db.delete_street(p["street_name"])
                db.print_db()

            if p["command"] == "GENERATE_GRAPH":
                graph = StreetGraph(db)
                graph.print_graph()

        except:
            sys.stderr.write("Error: Command parser doesn't work as expected\n")
            raise

    sys.exit(0)


if __name__ == "__main__":
    main()
