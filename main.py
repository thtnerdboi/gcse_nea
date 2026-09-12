import flightschedulegenerator as fsg
import visualisation
from simulation import Simulation

schedule = fsg.Schedule().create_schedule()

simulation = Simulation()
simulation.setup(100)

gui = visualisation.Visualisation()
gui.full_display(schedule, simulation)