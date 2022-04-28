from lib.sbs_utils.spaceobject import SpaceObject
from resourceasteroid import ResourceTypes
from lib.sbs_utils.consoledispatcher import MCommunications
from lib.sbs_utils.spaceobject import MSpawnActive
import sbs



class Spacedock(SpaceObject, MSpawnActive, MCommunications):
    ds_id = 0

    def __init__(self):
        super().__init__()

        Spacedock.ds_id += 1
        self.ds_id = Spacedock.ds_id
        self.comms_id =  f"DS {self.ds_id}"
        self.storage = {
            ResourceTypes.ENERGY: 0,
            ResourceTypes.MINERAL: 0,
            ResourceTypes.RARE_METAL: 0,
            ResourceTypes.ALLOY: 0,
            ResourceTypes.FOOD: 0,
        }

    def spawn(self, sim, x, y, z, side):
        super().spawn(sim,x,y,z,self.comms_id, side, "Starbase", "behav_station",)
        self.enable_comms()
    
    def deposit_storage(self, resource: ResourceTypes, amount: int):
        self.storage[resource] += amount

    def withdraw_storage(self, resource: ResourceTypes, amount: int):
        if self.storage[resource] >= amount:
            self.storage[resource] -= amount
            return True
        return False


    def comms_selected(self, sim, player_id):
        # if Empty it is waiting for what to harvest
        sbs.send_comms_selection_info(player_id, self.face_desc, "green", self.comms_id)

        sbs.send_comms_button_info(player_id, "blue", "Status", "status")
        sbs.send_comms_button_info(player_id, "red", "Build Nuke", "nuke")
        sbs.send_comms_button_info(player_id, "gold", "Build Harvester 10kA , 10kR", "havester")


    def comms_message(self, sim, message, player_id):
        
        match message:
            case "status":
                status = f"""
                Status: 
                    Energy: {self.storage[ResourceTypes.ENERGY]}" 
                    Mineral: {self.storage[ResourceTypes.MINERAL]}
                    Rare Metals: {self.storage[ResourceTypes.RARE_METAL]}
                    Alloy: {self.storage[ResourceTypes.ALLOY]}
                    Food: {self.storage[ResourceTypes.FOOD]}
                """
                
                sbs.send_comms_message_to_player_ship(player_id, 
                    self.id, "blue",
                    self.face_desc, f'{self.comms_id} > Artemis',
                    status,
                    "Station")
   

