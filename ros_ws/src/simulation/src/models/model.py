import abc
from numpy import array


class SimulationModel(object):
    """Abstract class for models for simulation"""

    def __init__(self, x=0, y=0, dt=0.1, speed=1):
        super(SimulationModel, self).__init__()
        self.x = 0
        self.y = 0
        self.X = array([self.x, self.y])
        self.dt = dt
        self.speed = speed

    @abc.abstractmethod
    def draw(self):
        " Function to draw the model at its current position"

    @abc.abstractmethod
    def simulate(self, u, env_conditions):
        "Simulates the model with a command u for dt"

    @abc.abstractmethod
    def fdot(self, u):
        "How to compute the evolution function of the model"
