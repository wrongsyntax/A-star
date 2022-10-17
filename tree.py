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


def create_safe_waypoints(nodes: dict, margin: float = 1.3):
    """
    Apply a safety margin to nodes so connections can be made without being on the border of the restricted region,
    while preserving the name associated with each waypoint.

    :param nodes: A dictionary of nodes that has the form {'waypoint_name': (x, y, classification)}
    :param margin: Amount to scale the restricted region by to provide a safety margin so the drone doesn't
        accidentally enter the restricted region.
    :return: A dictionary containing each waypoint name and its corresponding safe waypoint. Also return the
        restricted_region polygon for later use.
    """

    # list of (x,y) of obstacle bounds
    restricted_vertices = [(node[0], node[1]) for node in nodes.values() if node[2] == 'obstacle']
    restricted_region = sp.Polygon(*restricted_vertices)

    safe_waypoints = dict()
    # list of (x,y) of START and TARGET
    for name, data in nodes.items():
        if data[2] != 'obstacle':
            safe_waypoints[name] = (data[0], data[1])

    safe_region = restricted_region.scale(margin, margin, restricted_region.centroid)

    # ensure the safe_region is not so large that START or TARGET are inside
    # TODO: Ensure safe_region does not enclose START and TARGET

    # extend waypoints to also include safe vertices
    # IMPORTANT: this assumes that the order of points is maintained throughout this whole process
    i = 0
    for name, data in nodes.items():
        if name not in safe_waypoints:
            safe_waypoints[name] = (safe_region.vertices[i].x, safe_region.vertices[i].y)
            i += 1
        else:
            pass

    return safe_waypoints, restricted_region


def find_valid_connections(safe_waypoints: dict, restricted_region: sp.Polygon):
    """
    Finds all connections between any two nodes in the given data that don't intersect the polygon bounded by the
    vertices labelled 'obstacle'.

    :param restricted_region: The region bounded by the 'obstacle' waypoints that must be avoided
    :param safe_waypoints: A dictionary of waypoints and their names that has the safety margin applied
    :return: A list containing every two points that can be connected without intersecting the restricted region. Each
        pair of points is a tuple containing the names of the first and second waypoint that can be connected.
    """

    # gives a list of all possible combinations of points
    combos = list(combinations(safe_waypoints.values(), 2))

    valid_connections = []
    waypoint_names = list(safe_waypoints.keys())
    waypoint_values = list(safe_waypoints.values())

    for combo in combos:
        intersect = sp.intersection(sp.Segment(*combo), restricted_region)
        if not intersect:
            # find first waypoint name
            first = waypoint_values.index(combo[0])
            # find second waypoint name
            second = waypoint_values.index(combo[1])
            # append ('first', 'second') to valid_connections
            valid_connections.append((waypoint_names[first], waypoint_names[second]))

    return valid_connections


if __name__ == "__main__":
    parsed_nodes = parse_data("data.csv")
    waypoints, nofly_region = create_safe_waypoints(parsed_nodes)
    connections = find_valid_connections(waypoints, nofly_region)
    print(len(connections), connections)
