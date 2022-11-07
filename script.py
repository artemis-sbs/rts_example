import sbslibs
from sbs_utils.objects import Npc
import sbs
import sbs_utils.scattervec as scattervec
from harvester import Harvester, ResourceAsteroid
from sbs_utils.vec import Vec3
from sbs_utils.gui import Gui, Page
from spacedock import Spacedock
from player import Player
from sbs_utils.pages.start import ClientSelectPage, StartPage


from sbs_utils.handlerhooks import *


class Enemy(Npc):
    pass


class Mission:
    def add_asteroids(sim, g, name):
        landmark = None
        for v in g:
            asteroid = ResourceAsteroid()
            asteroid.spawn(sim, v)

            if landmark is None:
                landmark = sim.add_navpoint(v.x, v.y+100,v.z, name, "yellow");


    def start(sim, _):
        sbs.create_new_sim()
        sbs.resume_sim()
        
              
        v = Vec3(0,0,0)
        Player().spawn_v(sim, v, "Artemis", "TSN", "Battle Cruiser")
        
        Enemy().spawn_v(sim, Vec3(1000,0,100),"BAD GUY", "WTF", "Leviathan", "behav_npcship")

        Harvester().spawn(sim, Vec3(700,0,0), "TSN")
        Harvester().spawn(sim, Vec3(-700,0,0), "TSN")

        Spacedock().spawn(sim, Vec3(5000, 0, 5000), "TSN")
        Spacedock().spawn(sim, Vec3(-5000,0, 5000), "TSN")
        Spacedock().spawn(sim, Vec3(5000,0, -5000), "TSN")
        Spacedock().spawn(sim, Vec3(-5000,0,-5000), "TSN")

        # making a bunch of asteroids
        Mission.add_asteroids(sim, scattervec.line(10, Vec3(-2000,0,0), Vec3(2200,0, 1000),True), "line RND")
        Mission.add_asteroids(sim, scattervec.arc(20, Vec3(-2000,0,0), 500, 0, 45,False), "Arc")
        Mission.add_asteroids(sim, scattervec.ring(4,4, Vec3(-2000,0,-1000), 800, 100, 0, 160,True), "ring rnd")
        Mission.add_asteroids(sim, scattervec.ring_density([2, 4, 20], Vec3(2000,0,-1000), 800, 200, 0, 360,False), "ring density")
        Mission.add_asteroids(sim, scattervec.sphere(50, Vec3(0,0,4000), 400), "sphere")
        Mission.add_asteroids(sim, scattervec.sphere(50, Vec3(-2000,0,2000), 200, 800, ring=True), "sphere-Ring")
        Mission.add_asteroids(sim, scattervec.rect_fill(5,5, Vec3(2000,0, 4000), 500, 500, True), "Grid")
        Mission.add_asteroids(sim, scattervec.box_fill(5,5,5,  Vec3(-2000, 0, 4000), 500, 500,500), "Box")


def start_page():
    return StartPage("Mission: SBS_Example.^^This is an Example starter project", Mission.start)

Gui.server_start_page_class(start_page)
Gui.client_start_page_class(ClientSelectPage)


