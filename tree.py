import csv
from itertools import combinations

import sympy as sp


def parse_data(filename: str):
    """
    Parses the given csv file so the data is more easily accessible later on.

    :param filename: Input .csv file with the header "waypoint_name, x_position, y_position, type".
    :return: A dictionary that stores each 'waypoint_name' as the key and a tuple (x_pos: int, y_pos: int,
        classification: string) as the value.
    """

    nodes = {}

    with open(filename, newline='') as infile:
        data_reader = csv.reader(infile)
        next(data_reader, None)  # skip the headers
        for row in data_reader:
            try:
                nodes[row[0]] = (int(row[1]), int(row[2]), row[3])  # nodes = {'waypoint_name': (x, y, classification)}
            except ValueError:
                print(f"ValueError occurred in parse_data for loop.")

    return nodes


def find_valid_connections(nodes: dict, margin: float = 1.3):
    """
    Finds all connections between any two nodes in the given data that don't intersect the polygon bounded by the
    vertices labelled 'obstacle'.
    TODO: find a way to correlate the new safe waypoints with the original 'waypoint_name'

    :param margin: Amount to scale the restricted region by to provide a safety margin so the drone doesn't
        accidentally enter the restricted region.
    :param nodes: Dictionary of parsed nodes from parse_data(): {'waypoint_name': (x, y, classification)}
    :return: A list containing every two points that can be connected without intersecting the restricted region. Each
        pair of points is a list of two tuples representing (x, y).
    """

    # list of (x,y) of obstacle bounds
    restricted_vertices = [(node[0], node[1]) for node in nodes.values() if node[2] == 'obstacle']
    restricted_region = sp.Polygon(*restricted_vertices)

    # list of (x,y) of START and TARGET
    waypoints = [sp.Point((node[0], node[1])) for node in nodes.values() if node[2] != 'obstacle']

    safe_region = restricted_region.scale(margin, margin, restricted_region.centroid)
    # ensure the safe_region is not so large that START or TARGET are inside
    # TODO: This is not working yet
    if safe_region.encloses_point(waypoints[0]) or safe_region.encloses_point(waypoints[1]):
        return "!! Margin factor too large."

    # extend waypoints to also include safe vertices
    waypoints.extend(safe_region.vertices)

    # gives a list of all possible combinations of points
    combos = list(combinations(waypoints, 2))

    valid_connections = []

    for combo in combos:
        intersect = sp.intersection(sp.Segment(*combo), restricted_region)
        if not intersect:
            valid_connections.append([i.args for i in combo])

    return valid_connections


if __name__ == "__main__":
    parsed_nodes = parse_data("data.csv")
    print(find_valid_connections(parsed_nodes, margin=1.3))
    # print(find_valid_connections(parsed_nodes, 100))
