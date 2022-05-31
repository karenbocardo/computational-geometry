from matplotlib import pyplot as plt
from celluloid import Camera
from intersections import *

def separate(points):
    x, y = [], []
    for point in points:
        x.append(point.x)
        y.append(point.y)
    return x, y

fig = plt.figure()
ax1 = plt.gca()
camera = Camera(fig)



not_visited_color = "palevioletred"
visited_color = "mediumpurple"
convex_color = "steelblue"

def plot_frame():
    for segment in segments:
        x, y = separate([segment.sup, segment.inf])
        plt.plot(x, y, color='steelblue')
    camera.snap()

def plot_frame(convex, index):
    # not visited
    #plt.scatter(all_x, all_y, color = not_visited_color)
    convex_x, convex_y = separate(convex)
    plt.plot(convex_x, convex_y, color = 'grey')

    # visited and not in convex hull
    #if index < 0: x_list, y_list = all_x[index:], all_y[index:]
    #else: x_list, y_list = all_x[:index], all_y[:index]
    #plt.scatter(x_list, y_list, color = visited_color)

    # visited and in convex hull
    plt.scatter(convex_x, convex_y, color = convex_color)

    camera.snap()

#plt.plot([0,1], [0,1], color='steelblue')
#camera.snap()

ax1 = plt.gca()

ax1.scatter([0,1], [0,1], s=100, marker="x", linewidths=2) # segment start and ends
ax1.plot([0,1], [0,1], color='steelblue')

# plot horizontal sweep line
xlim = ax1.get_xlim()
ax1.plot(list(xlim), [1, 1], color="red")
#plt.plot(list(xlim), [1, 1], color="red")

camera.snap()

ax1.scatter([0,1], [0,1], s=100, marker="x", linewidths=2) # segment start and ends
ax1.plot([0,1], [0,1], color='steelblue')

# plot horizontal sweep line
xlim = ax1.get_xlim()
ax1.plot(list(xlim), [0,0], color="red")
#plt.plot(list(xlim), [1, 1], color="red")

camera.snap()

animation = camera.animate(interval = 300, repeat = True, repeat_delay = 500)
animation.save('animation.gif')