import wafer_simulator

sim = wafer_simulator.WaferSimulator(0.1, 1.0)
sim.setSpeed(1.0)

for i in range(30):
    sim.update()
    print(sim.getPosition())