from enum import IntEnum
from lib.sbs_utils.spaceobject import SpaceObject, MSpawnActive
from lib.sbs_utils.damagedispatcher import DamageDispatcher
from lib.sbs_utils.consoledispatcher import MCommunications
from lib.sbs_utils.tickdispatcher import TickDispatcher
from spacedock import Spacedock
from resourceasteroid import ResourceTypes, ResourceAsteroid

import sbs


class HarvesterState(IntEnum):
    UNKNOWN = 0
    EMPTY_WAITING = 1
    EMPTY  = 2
    HARVESTING = 3
    FULL_WAITING = 4
    FULL = 5
    RETURNING = 6
    EMPTYING = 7

class Harvester(SpaceObject, MSpawnActive, MCommunications):
    def __init__(self):
        self.amount = 0
        self.storage = 4000
        self.state = HarvesterState.UNKNOWN
        self.resource_type = ResourceTypes.ENERGY
        
    def spawn(self, sim, x: float, y: float ,z: float, side):
        ship = super().spawn(sim,x,y,z, None, side,  "Cargo", "behav_npcship")
        self.comms_id = f"{side} {self.id}"
        DamageDispatcher.add_source(self.id, self.on_damage_source)
        self.enable_comms(f"ter #964b00 8 1;ter #968b00 3 0;ter #968b00 4 0;ter #968b00 5 2;ter #fff 3 5;ter #964b00 8 4;")
        self.state = HarvesterState.EMPTY_WAITING
        return ship

    def on_damage_source(self, sim, damage_event):
        roid = SpaceObject.get_as(damage_event.target_id, ResourceAsteroid)

        if roid is None:
            # not targeting an asteroid
            return

        if self.state != HarvesterState.HARVESTING:
            # not harvesting so skip
            return

        if roid.amount < 50:
            self.find_target(sim)
        if self.amount >= self.storage:
            sbs.send_comms_message_to_player_ship(
                0, self.id, "green", self.face_desc, self.comms_id, 
                "Cargo hold full!", "harvester")
            self.state = HarvesterState.FULL_WAITING
            self.find_target(sim)
        else:
            roid.amount -= 50
            self.amount += 50
            per = 100*(self.amount/self.storage)
            if per % 10 == 0:
                sbs.send_comms_message_to_player_ship(
                    0, self.id, "yellow", self.face_desc, self.comms_id, 
                    f"{per}% filled", "status")

    def find_target(self, sim):
        if self.state == HarvesterState.HARVESTING:
            self.target_closest(sim,'ResourceAsteroid', filter_func=self.filter_res)
        elif self.state == HarvesterState.FULL_WAITING:
            self.clear_target(sim)
            self.comms_selected(sim, 0) ## THIS IS THE WRONG PLAYER ID

    def filter_res(self, other):
        if not isinstance(other[1], ResourceAsteroid):
            return False
        if other[1].amount <= 0:
            return False
        return other[1].resource_type == self.resource_type

    def think(self, sim, task):
        if self.state == HarvesterState.RETURNING:
            test = sbs.distance_id(self.id, task.base_id)
            if test < 600:
                self.state = HarvesterState.EMPTYING
                # change delay to 5 sec
                task.delay = 2
        elif self.state == HarvesterState.EMPTYING:
            self.amount -= 100
            base = SpaceObject.get(task.base_id)
            if base is not None:
                base.deposit_storage(self.resource_type,100)
                per = 100*(self.amount/self.storage)
                if per % 10 == 0:
                    sbs.send_comms_message_to_player_ship(
                        0, self.id, "yellow", self.face_desc, self.comms_id, 
                        f"Emptying {per}% left", "status")
            if self.amount <= 0:
                self.state = HarvesterState.EMPTY_WAITING
                task.stop()
                sbs.send_comms_message_to_player_ship(
                    0, self.id, "green", self.face_desc, self.comms_id, 
                    f"Empty", "status")


    def comms_selected(self, sim, player_id):
        # if Empty it is waiting for what to harvest
        sbs.send_comms_selection_info(player_id, self.face_desc, "green", self.comms_id)
        
        if self.state == HarvesterState.EMPTY_WAITING:
            sbs.send_comms_button_info(player_id, "blue", "Harvest energy", "get_energy")
            sbs.send_comms_button_info(player_id, "red", "Harvest minerals", "get_mineral")
            sbs.send_comms_button_info(player_id, "gold", "Harvest rare metals", "get_rare")
            sbs.send_comms_button_info(player_id, "silver", "Harvest alloys", "get_alloy")
            sbs.send_comms_button_info(player_id, "green", "Harvest replicator fuel", "get_food")

        if self.state == HarvesterState.FULL_WAITING:
            for base in self.find_close_list(sim, 'Spacedock'):
                sbs.send_comms_button_info(player_id, "yellow", f"Head to {base.obj.comms_id}", f"{base.obj.id}")


    def comms_message(self, sim, message, player_id):

        if message.isnumeric():
                other_id = int(message)
                self.target(sim,other_id, False)
                # every ten seconds r
                self.tsk = TickDispatcher.do_interval(sim,self.think, 5)
                self.tsk.base_id = other_id
                self.state = HarvesterState.RETURNING
                return

        match message:
            case 'get_energy':
                self.resource_type = ResourceTypes.ENERGY
                self.send_comms('Gathering energy', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target(sim)
            case 'get_mineral':
                self.resource_type = ResourceTypes.MINERAL
                self.send_comms('Gathering minerals', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target(sim)
            case 'get_rare':
                self.resource_type = ResourceTypes.RARE_METAL
                self.send_comms('Gathering rare metals', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target(sim)
            case 'get_alloy':
                self.resource_type = ResourceTypes.ALLOY
                self.send_comms('Gathering alloys', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target(sim)
            case 'get_food':
                self.resource_type = ResourceTypes.FOOD
                self.send_comms('Gathering replicator fuel', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target(sim)
            case '_':
                return

        # Clear buttons?
        sbs.send_comms_selection_info(player_id, self.face_desc, "green", self.comms_id)

        

    def send_comms(self, message, color='green', player_id=0):
        sbs.send_comms_message_to_player_ship(
                    player_id, self.id, color, 
                    self.face_desc, self.comms_id, 
                    message, 
                    "harvester")
