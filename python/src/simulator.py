<<<<<<< Updated upstream
import wafer_simulator

sim = wafer_simulator.WaferSimulator(0.1, 1.0)
sim.setSpeed(1.0)

for i in range(30):
    sim.update()
    print(sim.getPosition())
=======
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from simulator import wafer_simulator

# Create simulator
sim = wafer_simulator.WaferSimulator(0.05, 10.0, 10.0)

# Lists to store trail
xdata, ydata = [], []

limitX, limitY = sim.getLimits()

print(sim.getLimits())

# Set up figure
fig, ax = plt.subplots()
ax.set_xlim(-limitX, limitX)
ax.set_ylim(-limitY, limitY)
ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.set_title("Wafer Simulator with Trail")

# Point and trail line
point, = ax.plot([], [], 'ro')       # red moving point
trail, = ax.plot([], [], 'b-', lw=1) # blue trail line

sim.setForce(1,0)

def update(frame):
    sim.update()
    x, y = sim.getPosition()
    print(x,y)
    # Update point
    point.set_data([x], [y])
    
    # Update trail
    xdata.append(x)
    ydata.append(y)
    trail.set_data(xdata, ydata)
    
    return trail, point

ani = animation.FuncAnimation(fig, update, frames=500, interval=20, blit=True)
plt.show()
>>>>>>> Stashed changes
