from matplotlib import pyplot as plt  # for plotting

fig = plt.figure()# create a figure
ax = fig.add_subplot(1,1,1)


def animate(convex_hull, points,centr=None): # for animation
    ax.clear() #clear figure each time when call  DELETE TO SHOW POLYLABEL WORK
    xs, ys = zip(*points)  # unzip into x and y coord lists
    ax.scatter(xs, ys)

    if convex_hull != None: # add lines of the hull
        for i in range(1, len(convex_hull)):
            c0 = convex_hull[i - 1]
            c1 = convex_hull[i]
            ax.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')

    if centr != None: #add circle to plot
        ax.scatter(centr[0][0], centr[0][1], color='green')
        plt.annotate("Real centr", (centr[0][0], centr[0][1]))
        circle = plt.Circle(centr[0], centr[1], fill = False)
        ax1 = plt.gca()
        ax1.add_patch(circle)
        plt.axis('scaled')
