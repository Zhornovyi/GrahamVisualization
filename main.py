from Graham_hull import create_points, graham_scan, build_hull_list, build_hull
from animation import fig, animate
from polylabel import polylabel
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt  # for plotting

def main():
    pts = create_points(10)
    print("Points:", pts)
    anchor, sorted_pts = graham_scan(pts)
    hull = build_hull_list(anchor, sorted_pts)
    centr = polylabel([hull], with_distance = True)
    ani = FuncAnimation(fig, animate, frames= build_hull(anchor,sorted_pts), fargs= (pts,centr), interval=500, repeat=False)
    plt.show()
if __name__ =="__main__":
    main()
