"""Scenic World Model for GFootball Scenarios."""

from scenic.simulators.gfootball.simulator import GFootBallSimulator

# Set up workspace
width = 2
length = 0.42*2
workspace = Workspace(RectangularRegion(0 @ 0, 0, width, length))

# types of objects

class Ball:
    position: Point on workspace
    direction: Range(0, 360) deg

class Player:
    position: Point on workspace
    direction: Range(0, 360) deg
    width: 0.01
    length: 0.01