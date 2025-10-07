from wafer_simulator import simulator

w = simulator.WaferSimulator(deltaT=0.1, speed=0.5, limit=1.0)
w.update()
print(w.get_position())