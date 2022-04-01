
"""
valtert 2022 (c)
SRP Aalborghus Gymnasium

Lånt kode fra:
    https://www.pygame.org/ distribueret under GNU LGPL version 2.1
        https://www.gnu.org/copyleft/lesser.html


MODELLERINGS FORMÅL:
    Varme udbredelse som bølger
    Varme udbredelse i farver
    Varme målinger i tid

MODELLERINGS GUI "ANSIGT":

---------------------------------
|            |   |              |
|   kilde    |   |     måler    |
|            |   |              |
|            -----              |
|                               |
---------------------------------

Her ses en fx beton væg med en varme kilde på den ene side og en måler på den
anden side.

På farvemålerne burde man kunne se hvordan varmen udbredes i forhold til farve.
Altså længste punkt er rødt.


METODE:
    fx. 1px = 1cm^2.
    Så 1000x600px er 10 meter og 6 meter.

    Der placeres en eller flere varmekilder som udsender varme.
    Varmen udbredes derefter på en pixel basis.
    Varmen kan kun nå så langt indtil den har omsat alt til rumtemperatur.

    cellular automata


FYSIK:
    Udlignelse af varme

    Termondynamikkens love specielt:
        Termondynamikkens 0. lov
        + https://en.wikipedia.org/wiki/Thermal_equilibrium

    E = m * c * dT

    https://fysikleksikon.nbi.ku.dk/t/termodynamik/
    Newton's law of cooling

    Fourier's law
    https://www.smlease.com/entries/thermal-design/conduction-conductive-heat-transfer/

    https://www.thermal-engineering.org/what-is-heat-transfer-definition/
    https://www.sciencedirect.com/topics/engineering/heat-conduction
    https://www.sciencedirect.com/topics/engineering/radiation-heat-transfer

    En konstant omkring
    https://en.wikipedia.org/wiki/Thermal_transmittance

    Der findes tre forskellige måder at varme transformation:
        Radiation (varmestråling) https://fysikleksikon.nbi.ku.dk/v/varmestraaling/
        Convection (varmekonvektion) https://fysikleksikon.nbi.ku.dk/v/varmekonvektion/
        Conduction (varmeledning) https://fysikleksikon.nbi.ku.dk/v/varmeledning/
    Alle disse er taget højde for i "heat transfer coeffecient"

    Det kan fåes ved
    Φ (phi) = A * U * (T1 - T2),
    where:
        Φ: heat transfer [Φ] = Watt,
        U: thermal transmittance [U] = W/(m^2*K) K  <= kendt på forhånd
        T1: temperature on one side of the structure
        T2: temperature on the other side of the structure
        A: area in square metres.

    Meget spændende og meget højt niveau.
    http://www-personal.umich.edu/~kaviany/course/HTP/Introduction_to_HTP.pdf

    https://backend.orbit.dtu.dk/ws/portalfiles/portal/142939049/2018_Januar_Termodynamik.pdf
    Kig fx på 5.5.4

    I simuleringing skal jeg nok holde mig til det makroskopiske niveau
    https://webkemi.dk/Conductivity/ThermalConductivity.htm

    Formel til absorption af energien fra en temparetur til en anden. Kan også bruges omvendt
    https://www.thermal-engineering.org/what-is-heat-absorption-definition/

    Entropy, ting sker tilfældigt. Det vigtigt at vide at varmeoverførlese sker tilfældigt.
    https://en.wikipedia.org/wiki/Entropy

    "the heat equation"
    https://tutorial.math.lamar.edu/Classes/DE/TheHeatEquation.aspx


    Løsninger af differenital ligningen "the heat equation" for specefikke eksempler
    http://wendl.weebly.com/textbook.html


    https://energy.concord.org/energy2d/      m/ forklaring:
    https://charlesxie.medium.com/numerical-algorithms-for-simulating-three-modes-of-heat-transfer-e65fca9baf50


    Simulering breakdown "nodal network"
    https://www.visualslope.com/Library/FDM-for-heat-transfering.pdf

    Simulering i excel
    https://upcommons.upc.edu/bitstream/handle/2099.1/14576/Final%20Thesis_Luis%20Garcia%20Blanch.pdf

    Conduction (varmeledning) https://fysikleksikon.nbi.ku.dk/v/varmeledning/



NOTER:
    Følger pythons syntakts. Altså at classes starter med Stort og
    konstanter med FULD STORT.
    Altså hvis E = m * c, være self.energy = self.mass * osv.



KODE DER IKKE BLIVER BRUGT
def fourier_law():
    ""
    Heat transfer: Qc = - K * A * (dT / L)
    Where:
        Q: conductive heat transfer per unit of time [Q] = Watt
        K: Material thermal conductivity [K] = W/mK
        dT: temperatur differenital [T] = C el. K
        L: Length (af materialet)

    NOTE:
        resultatet målt i Watt kan derefter indgå i
        P = dE/dt, hvis en af de to kendes
    ""

    pass


VERSION 0.0.1
    Varme fordeling uden reele værdier
    Hver celle har egen energi
    Hver celle levere energi til de omgivende celler.
    Hver celle levere energi med en effekt på 2W
    Bare et tomt rum.

https://www.danskbetonforening.dk/media/pdf2009/beton_termiske_egenskaber_indeklima.pdf

"""

### libs ###
import pygame as pg
from colors import *
from random import shuffle
import time
import math
from copy import deepcopy
from filter import makeup
from plot import render_3d_plot
import os

color = Gradient (0, 30, [
        (8, 124, 190),
        (26, 129, 176),
        (43, 134, 163),
        (61, 139, 149),
        (79, 144, 136),
        (96, 149, 122),
        (114, 154, 109),
        (132, 159, 95),
        (149, 163, 81),
        (167, 168, 68),
        (184, 173, 54),
        (202, 178, 41),
        (220, 183, 27),
        (237, 188, 14),
        (255, 193, 0),
        (250, 180, 1),
        (246, 167, 1),
        (241, 153, 2),
        (236, 140, 2),
        (232, 127, 3),
        (227, 114, 3),
        (223, 101, 4),
        (218, 87, 5),
        (213, 74, 5),
        (209, 61, 6),
        (204, 48, 6),
        (199, 34, 7),
        (195, 21, 7),
        (190, 8, 8)
    ],
)

# Disse konstanter burde ændre sig i forhold til 
# Hvilken grid størrelse der bruges...
# Eller er dette en design princip?
AREA = 1
NODE_BRIDGE_LENGTH = 0.5
NODE_HEAT_CAPACITY = 1
NODE_MASS = 0.001
VOLUME = NODE_BRIDGE_LENGTH * NODE_BRIDGE_LENGTH * 2.5 #m^3
start_temperature = [0]
basedir_sim = ['']

def heat_storage_transport_equation(t, h, g, c, tr, tl, tu, td):
    """
    ref: https://excelunusual.com/wp-content/uploads/2011/03/2D_Heat_Transfer_Tutorial_1.pdf

    dQ = C * dT
    dQ/dt = G * (T_1 - T_2)

    T_n(m+1) = T_n(m) + ( [h*G_int]/C ) * ( T_right(m) + T_front(m) + T_left(m) + T_back - 4 * T_n(m) )

    """

    return h*g/c * (tr + tl + tu + td - 4 * t)


def heat_transfer(t:float, c, *n):
    """
    Hvert celle er en node ikke et materiale.
    Materialet er imellem men det for ikke varme men derimod
    overholder bare isolaions reglerne. jf. "varme til husbehov"

    Q = k * A dT * dt

    """

    n = [*n] #create list because tuple is imutable
    shuffle(n) #shuffle so to not create a favor in one direction

    for cell in n:
        if cell.temp <= 0 or c.temp >= cell.temp:
            continue

        # fouries heat equation
        q = max(c.k * AREA * (cell.temp - c.temp) * t, 0)

        qTdiff = calc_temperature_diff(NODE_MASS, NODE_HEAT_CAPACITY, q)
        cell.temp -= qTdiff

        # da dT kan være for stor, kan en for stor energi afgives, så temperaturen bliver negativ
        # der skal dog stadig afgives noget energi, dette bliver halvdelen af energi fra cellen
        # istedet for halvdelen kunne det også være et tilfædig værdi
        if cell.temp < 0:
            q = calc_energy_diff(NODE_MASS, NODE_HEAT_CAPACITY, cell.temp + qTdiff) / 2 #get energy before
            qt = calc_temperature_diff(NODE_MASS, NODE_HEAT_CAPACITY, q)
            cell.temp = qt

        #cell.temp = max(cell.temp, 0)

        c.temp += calc_temperature_diff(NODE_MASS, NODE_HEAT_CAPACITY, q)


def calc_energy_diff(mass:float, heat_capacity:float, temperature:float) -> float:
    """
    calculate E(m,c,T) = m * C * T

    parameteres:
        mass:float [m] = kg
        heat_capacity:float [c] = J/(kg*C)
        temperature:float [T] = C

    return:
        energy:float [m] = J
    """

    return mass * heat_capacity * temperature


def calc_temperature_diff(mass:float, heat_capacity:float, energy:float) -> float:
    """
    calculate E(m,c,T) = m * C * T

    parameteres:
        mass:float [m] = kg
        heat_capacity:float [c] = J/(kg*C)
        energy:float [m] = J

    return:
        temperature:float [T] = C
    """

    if mass * heat_capacity == 0:
        return 0

    return energy / (mass * heat_capacity)


heat_cells = []
class Cell:
    """
    docstring for Cell

    Every material class should inheriet from this class
    """

    def __init__(self, pos):
        #self.energy = 0
        self.pos = pos
        self.color = [255,255,255]
        
        # for at give rum til at man kan sætte en "custom" temperatur ved loading. 
        #if not hasattr(self, 'temp'):
        #    self.temp = start_temperature[0]
        # get_real_temperature^-1
        self.temp = start_temperature[0]
        self.calculate_base_temp()

    def calculate_base_temp(self):
        self.temp = calc_temperature_diff(NODE_MASS, NODE_HEAT_CAPACITY, calc_energy_diff(self.mass, self.heat_capacity, self.temp))

    def get_real_temp(self):
        return min(self.temp,calc_temperature_diff(self.mass, self.heat_capacity, calc_energy_diff(NODE_MASS, NODE_HEAT_CAPACITY, self.temp)))

    def draw_under_layer(self, win, factor=1):
        self.color = color.get(self.temp)
        pg.draw.rect(win, self.color, [self.pos[0]*factor, self.pos[1]*factor, factor, factor])

    def draw(self, win, factor=1):
        self.color = color.get(self.get_real_temp())
        pg.draw.rect(win, self.color, [self.pos[0]*factor, self.pos[1]*factor, factor, factor])


    def update(self, sim):
        """
        The energy will be split up into the cells with less energy

        The energy will be given out according to the cell with lowest temperature.
        This could also be random using the shuffle.
        """

        try:
            heat_transfer (
                sim.tick,
                self,
                sim.get_node_by_pos(self.pos[0]+1, self.pos[1]),
                sim.get_node_by_pos(self.pos[0]-1, self.pos[1]),
                sim.get_node_by_pos(self.pos[0], self.pos[1]+1),
                sim.get_node_by_pos(self.pos[0], self.pos[1]-1),
            )

        except IndexError:
            pass

    def __repr__(self):
        return str(self.pos)

    def __int__(self):
        return int(self.get_real_temp())



class Air(Cell):
    """
    docstring for Air.

    Data from "Varme til husbehov"
    """

    def __init__(self, pos):
        self.heat_capacity = 1.005
        self.k = 0.024/NODE_BRIDGE_LENGTH
        self.mass = 1.204 * VOLUME
        super(Air, self).__init__(pos)


class Material(Cell):
    """
    docstring for Material.

    Data from http://www.danskbetonforening.dk/media/pdf2006/olsen.pdf
    """

    def __init__(self, hc, lamb, mass, pos):
        self.heat_capacity = hc
        self.k = lamb/NODE_BRIDGE_LENGTH
        self.mass = mass * VOLUME
        super(Material, self).__init__(pos)

    def get_properties(self):
        return self.heat_capacity, self.k, self.mass


class Heater(Cell):
    """docstring for Heater."""

    def __init__(self, pos, temp):
        self.heat_capacity = 1
        self.k = 1 / NODE_BRIDGE_LENGTH
        self.mass = VOLUME
        self.constant_temp = temp
        heat_cells.append(self)
        super(Heater, self).__init__(pos)
        self.temp = self.constant_temp

def convert(tfunc, val, fallback=None):
    try:
        return tfunc(val)
    except Exception as e:
        return fallback

class Simulation:
    """
    docstring for Simulation
    """

    def __init__(self, size=(200,200), upscale=1, settings={}):

        self.size = size
        self.upscale = convert(int,upscale, 1)

        # dt < 0.005
        self.tick = convert(float,settings.get('tick', 0.005), 0.005) #0.005 #1 second per update
        self.iterations = 0
        self.border_rect = [0,0,self.size[0]*self.upscale, self.size[1]*self.upscale]
        self.settings = settings

        # 2d reprsentation of the map stored in one array
        self.map = []
        """
        Hall of fame of small and effective code
        [self.map.extend([Air((j,i)) for j in range(self.size[0])]) for i in range(self.size[1])]
        """

        #self.set_node_at_pos(50,50, Heater((50,50), 20))

    def get_node_by_pos(self, x, y):
        if x < 0 or y < 0:
            raise IndexError
        return self.map[y*self.size[0]+x]

    def set_node_at_pos(self, x, y, node):
        self.map[y*self.size[0]+x] = node


    def update(self):
        self.iterations += 1

        l = [*self.map]
        shuffle(l)
        for cell in l:
            cell.update(self)
        for heater in heat_cells:
            heater.temp = int(heater.constant_temp)
            heater.calculate_base_temp()

    def draw(self):

        # refresh and draw over
        self.win.fill(color.get(0))

        #        leave unseen cells out of drawing calls
        for cell in self.map[self.size[0]:]:
            cell.draw(self.win, self.upscale)
        #for heater in heat_cells:
        #    heater.draw(self.win, self.upscale)

        # draw border
        pg.draw.rect(self.win, WHITE, self.border_rect, self.upscale, 1)
        pg.display.update()


    def _pygame_init_(self):
        pg.init()
        pg.display.set_icon(pg.image.load(os.path.join(basedir_sim[0], 'flames.png')))
        size = [*self.size]
        if self.upscale:
            size = [self.size[0] * self.upscale, self.size[1] * self.upscale]
        self.win = pg.display.set_mode(size)
        pg.display.set_caption("Udbredelse af varme i et 2D rum")
        self.clock = pg.time.Clock()


    def _show_result_(self):
        if self.settings.get('render3d'):
            self._render_3d_model_()

        if self.settings.get('filter'):
            original_upscaling = deepcopy(self.upscale)
            map = makeup(self.map,self.size,color,self.upscale)

            # reset information
            self.size = [len(map), len(map[0])]
            self.upscale = 0
        self._pygame_init_()

        if self.settings.get('filter'):
            # draw
            for row in range(len(map)):

                for col in range(len(map[row])):

                    pg.draw.rect(self.win, map[row][col], [col, row, 1,1])

            pg.draw.rect(self.win, WHITE, [0,0, len(map), len(map[0])], original_upscaling, 1)
            pg.display.update()
        else:
            self.draw()

        run = True
        while run:

            # run trough events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    #sys.exit()

            self.clock.tick(60) #force 60fps
            #pg.display.set_caption(str(self.iterations))

    def _render_3d_model_(self):
        render_3d_plot(self.map, self.size, color, basedir_sim[0])

    def _print_stats_(self):
        s = dround(time.time()-self.start_time, 2)
        m = dround(s/60, 2)
        h = dround(m/60, 4)
        print('Done! Took {} second(s) / {} minut(es) / {} hour(s)'.format(s, m, h))
        print('Simulation time: {} second(s)'.format(self.iterations*self.tick))


    def loop_animation_under_layer(self):

        # init gui
        self._pygame_init_()
        pg.display.set_caption('Udbredelse af varme i et 2D rum | Alle lag synlige')

        run = True
        while run:

            # run trough events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            self.update()
            self.win.fill(color.get(0))
            for cell in self.map[self.size[0]:]:
                cell.draw_under_layer(self.win, self.upscale)

            # draw border
            pg.draw.rect(self.win, WHITE, self.border_rect, self.upscale, 1)
            pg.display.update()
            self.clock.tick(60) #force 60fps


    def loop_animation(self):

        # init gui
        self._pygame_init_()

        run = True
        while run:

            # run trough events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            self.update()
            self.draw()

            self.clock.tick(60) #force 60fps
            cap = str(self.iterations)
            try:
                pos = pg.mouse.get_pos()
                mnode = self.get_node_by_pos(round(pos[0]/self.upscale), round(pos[1]/self.upscale))
                cap += ' / ' + str(dround(mnode.get_real_temp(), 4))
            except IndexError:
                pass
            cap += ' / ' + str(dround(self.iterations*self.tick,2)) + 's'
            pg.display.set_caption(cap)


    def simulation_dynamic(self, spot):

        run = True
        self.start_time = time.time()
        last_temp = 0
        node = self.get_node_by_pos(*spot[:2])

        while run:
            self.update()
            proc = math.floor((node.temp / spot[2]) * 100)
            if last_temp != proc:
                last_temp = proc
                if proc >= 100:
                    self._print_stats_()
                    print('{}% ({} / {})'.format(proc, dround(node.temp,2), spot[2]))
                else:
                    print('{}% ({} / {})'.format(proc, dround(node.temp,2), spot[2]))
            if node.temp >= spot[2]:
                run = False
                self._show_result_()


    def simulation_static(self, iterations=None, timer=None, progress=None):

        if timer:
            iterations = math.ceil(timer/self.tick)

        run = True
        self.start_time = time.time()
        last_proc = 0
        while run:
            self.update()
            proc = math.floor((self.iterations / iterations) * 100)
            if last_proc != proc:
                last_proc = proc
                if proc >= 100:
                    s = dround(time.time()-self.start_time, 2)
                    m = dround(s/60, 2)
                    h = dround(m/60, 4)
                    print('Done! Took {} second(s) / {} minut(es) / {} hour(s)'.format(s, m, h))
                    print('Simulation time: {} second(s)'.format(self.iterations*self.tick))
                else:
                    if progress:
                        if not progress(proc):
                            last_proc = 100
                            run = False
                    #print('{}% ({} / {})'.format(proc, self.iterations, iterations))
            if self.iterations >= iterations:
                run = False
        self._show_result_()


#Loader().load_json('map/test.json').simulation_dynamic([50,90,2])
#Loader(Simulation).load_json('map/test.json').simulation_static(iterations=1000,progress=lambda p:not print(p))
#Simulation().simulation_static(timer=20)
#Simulation().simulation_dynamic([50,10,10])
#Simulation().loop_animation()