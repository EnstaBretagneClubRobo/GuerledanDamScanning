from model import SimulationModel
import numpy as np


class Car(SimulationModel):
    """Simulation d'un char"""

    def __init__(self, x=0, y=0, theta=0, dt=0.1, speed=1):
        super(Car, self).__init__()
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = speed
        self.dt = dt
        # convert to np.float64 otherwise an int is not automatically converted during
        # augmented assignment
        self.X = np.array([x, y, theta], dtype=np.float64)
        self.img = np.array([[1, -1, 0, 0, -1, -1, 0, 0, -1, 1, 0, 0, 3, 3, 0],
                             [-2, -2, -2, -1, -1, 1, 1, 2, 2, 2, 2, 1, 0.5, -0.5, -1]])
        self.img = np.vstack(
            (self.img, np.ones(self.img.shape[1])))
        self.cmd_size = 2

    def draw(self):
        R = np.array([[np.cos(self.X[2]), -np.sin(self.X[2]), self.X[0]],
                      [np.sin(self.X[2]), np.cos(self.X[2]), self.X[1]],
                      [0, 0, 1]])

        self.img = np.dot(R, self.img)
        plt.plot(self.img[0], self.img[1])

    def fdot(self, u):
        xdot = self.speed * u[1] * np.cos(self.X[2])
        ydot = self.speed * u[1] * np.sin(self.X[2])
        thetadot = u[0]
        return np.array([xdot, ydot, thetadot])

    def simulate(self, speed, rot):
        # if len(u) != self.cmd_size:
        #     print "*** WARNING : WRONG CMD SIZE"
        self.X += self.fdot([rot, speed]) * self.dt
        # always wrap theta between -pi and pi
        self.X[2] = (self.X[2] + np.pi) % (2 * np.pi) - np.pi
        # self.X[2] = np.unwrap([0, self.X[2]])[1]
        self.x, self.y, self.theta = self.X
