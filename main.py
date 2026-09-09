import passenger
import visualisation
from simulation import Simulation

simulation = Simulation()
simulation.setup(100)

gui = visualisation.Visualisation()
gui.passenger_display(simulation)