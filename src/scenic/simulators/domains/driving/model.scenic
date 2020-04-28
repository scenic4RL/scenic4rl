"""Scenic world model for scenarios using the generic driving domain."""

from scenic.simulators.domains.driving.workspace import DrivingWorkspace
import scenic.simulators.domains.driving.network as networkModule

from scenic.simulators.gta.interface import CarColor    # TODO refactor

network = networkModule.network
workspace = DrivingWorkspace(network)

road = network.drivableRegion
sidewalk = network.sidewalkRegion
intersection = network.intersectionRegion

roadDirection = network.roadDirection

class Vehicle:
    regionContainedIn: road
    position: Point on road
    heading: (roadDirection at self.position) + self.roadDeviation
    roadDeviation: 0
    viewAngle: 90 deg
    color: [1, 0, 0]

class Car(Vehicle):
    width: 2
    height: 4.5
    color: CarColor.defaultColor()
