import matplotlib.pyplot as plt

import tree


# get all required data
parsed_nodes = tree.parse_data("data.csv")
waypoints, nofly_region = tree.create_safe_waypoints(parsed_nodes)

points_x = [i[0] for i in parsed_nodes.values()]
points_y = [i[1] for i in parsed_nodes.values()]
print(f"{points_x = }\n{points_y = }")

print(f"{waypoints = }")
safe_x = [i[0] for i in waypoints.values()]
safe_y = [i[1] for i in waypoints.values()]
names = [i for i in waypoints.keys()]
for i in range(len(waypoints)):
    x = safe_x[i]
    y = safe_y[i]
    plt.plot(x, y, "bs")
    plt.text(x + 0.1, y + 0.1, names[i])

for side in nofly_region.sides:
    nofly_sides_x = []
    nofly_sides_y = []
    for point in side.points:
        nofly_sides_x.append(int(point.x))
        nofly_sides_y.append(int(point.y))
    plt.plot(nofly_sides_x, nofly_sides_y, "y")

print(f"{nofly_sides_x = }\n{nofly_sides_y = }")

# plot
plt.plot(points_x, points_y, "yo")

plt.axis('square')
plt.show()
