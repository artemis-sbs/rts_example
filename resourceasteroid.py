from enum import IntEnum
from random import randint
from lib.sbs_utils.spaceobject import SpaceObject, MSpawnPassive

class ResourceTypes(IntEnum):
    DIRT = 0
    # Processed
    ENERGY = 1
    MINERAL = 2
    RARE_METAL = 3
    ALLOY = 4
    FOOD = 5
    # RAW
    NOBLE_GAS = 6
    REACTIVE = 7
    ALKALI = 8
    METALLOID = 9
    ALKALINE_METAL = 10
    TRANSITION_METAL = 11
    POST_TRANSITION_METAL = 12


class ResourceAsteroid(SpaceObject, MSpawnPassive):

    def __init__(self) -> None:
        super().__init__()
        r = randint(1,12)

        # raw materials use random art
        self.art = r if r <6 else randint(6,11)

        self.amount = randint(1000,15000)
        self.resource_type = ResourceTypes(r)

    def spawn(self, sim, v):
        return super().spawn_v(sim, v, None, None, f"Asteroid {self.art}", "behav_asteroid")
        
        
