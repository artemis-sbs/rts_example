
from lib.sbs_utils.spaceobject import SpaceObject
import sbs
import lib.sbs_utils.scatter as scatter
from harvester import Harvester, ResourceAsteroid
from spacedock import Spacedock
from player import Player

from lib.sbs_utils.handlerhooks import *

class GuiMain:
    def __init__(self) -> None:
        self.gui_state = 'options'

    def present(self, sim):
        match self.gui_state:
            case  "sim_on":
                self.gui_state = "blank"
                sbs.send_gui_clear(0)

            case  "options":
                sbs.send_gui_clear(0)
                # Setting this to a state we don't process
                # keeps the existing GUI displayed
                self.gui_state = "presenting"
                sbs.send_gui_text(
                    0, "Mission: SBS_Example.^^This is an Example starter project", "text", 25, 30, 99, 90)
                sbs.send_gui_button(0, "Start Mission", "start", 80, 95, 99, 99)

    def on_message(self, sim, message_tag, clientID):
        match message_tag:
            case "continue":
                self.gui_state = "blank"

            case "start":
                sbs.create_new_sim()
                sbs.resume_sim()
                Mission.start(sim)



class Mission:
    main = GuiMain()

    def add_asteroids(sim, g, name):
        landmark = None
        for v in g:
            asteroid = ResourceAsteroid()
            asteroid.spawn(sim, v.x, v.y, v.z)

            if landmark is None:
                landmark = sim.add_navpoint(v.x, v.y+100,v.z, name, "yellow");


    def start(sim):
  
        Player().spawn(sim, 0,0,0, "Artemis", "TSN", "Battle Cruiser")

        Harvester().spawn(sim, 700,0,0, "TSN")
        Harvester().spawn(sim, -700,0,0, "TSN")

        Spacedock().spawn(sim, 5000, 0, 5000, "TSN")
        Spacedock().spawn(sim, -5000,0, 5000, "TSN")
        Spacedock().spawn(sim, 5000,0, -5000, "TSN")
        Spacedock().spawn(sim, -5000,0,-5000, "TSN")

        # making a bunch of asteroids
        Mission.add_asteroids(sim, scatter.line(10, -2000,0,0, 2200,0, 1000,True), "line RND")
        Mission.add_asteroids(sim, scatter.arc(20, -2000,0,0, 500, 0, 45,False), "Arc")
        Mission.add_asteroids(sim, scatter.ring(4,4, -2000,0,-1000, 800, 100, 0, 160,True), "ring rnd")
        Mission.add_asteroids(sim, scatter.ring_density([2, 4, 20], 2000,0,-1000, 800, 200, 0, 360,False), "ring density")
        Mission.add_asteroids(sim, scatter.sphere(50, 0,0,4000, 400), "sphere")
        Mission.add_asteroids(sim, scatter.sphere(50, -2000,0,2000, 200, 800, ring=True), "sphere-Ring")
        Mission.add_asteroids(sim, scatter.rect_fill(5,5,  2000,0, 4000, 500, 500, True), "Grid")
        Mission.add_asteroids(sim, scatter.box_fill(5,5,5,  -2000, 0, 4000, 500, 500,500), "Box")
        

def HandlePresentGUI(sim):
    Mission.main.present(sim)

def HandlePresentGUIMessage(sim, message_tag, clientID):
    Mission.main.on_message(sim, message_tag, clientID)



