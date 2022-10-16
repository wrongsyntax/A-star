import csv


def parse_data(filename):
    """
    Parses the given csv file so the data is more easily accessible later on.

    :param filename: input .csv file with the header "waypoint_name, x_position, y_position, type"
    :return: a dictionary that stores each 'waypoint_name' as the key and a tuple (x_pos: int, y_pos: int,
    classification: string)
    as the value
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


if __name__ == "__main__":
    parsed = parse_data("data.csv")
    print(parsed)
