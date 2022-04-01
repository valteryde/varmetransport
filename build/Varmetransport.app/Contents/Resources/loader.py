
import json
import time
from simulation import *

class Loader:
    """
    docstring for Loader.

    Loader assist with loading and parsing

    """

    def __init__(self):
        pass


    def load_json(self, path):

        # load and parse json
        f = open(path, 'r')
        j = json.loads(f.read())

        st = j["options"].get("start_temp")
        if convert(int,st):
            start_temperature[0] = int(st)

        # create sim
        h, w = len(j["body"]), len(j["body"][0])
        c = int(j["options"]["cell"])
        if convert(int,j["options"].get("upscale", 'not a int')):
            up = j["options"].get("upscale")
        else:
            up = math.floor(600/(w*c))
        sim = Simulation((h*c, w*c), up, settings=j['options'])

        # set options (could be a security problem)
        if j["options"].get("upscale"):
            del j["options"]["upscale"]

        # run throuh map
        for row_num in range(h):

            for col_num in range(w):
                cell = j["material"][str(j["body"][row_num][col_num])]
                type_ = cell["type"]

                pos = (col_num, row_num)
                if type_ == 'air':
                    sim.map.append(Air(pos))
                elif type_ == 'heater':
                    sim.map.append(Heater(pos, cell["value"]))
                elif type_ == 'warmth':
                    mat_cell = Air(pos)
                    mat_cell.temp = int(cell["value"])
                    mat_cell.calculate_base_temp()
                    sim.map.append(mat_cell)
                else:
                    sim.map.append(Material(cell['heatcapacity'],cell["lambda"], cell["density"], pos))

        f.close()

        # upscaling. Creating a larger map
        if c > 1:
            newmap = [[0 for j in range(w*c)] for i in range(h*c)]

            for cell in sim.map:

                for i in range(c):
                    for j in range(c): #av av på nested loops
                        pos = (cell.pos[0]*c + i,cell.pos[1]*c + j)
                        if type(cell) == Air:
                            c_ = Air(pos)
                            c_.temp = cell.temp
                        elif type(cell) == Heater:
                            c_ = Heater(pos, deepcopy(cell.constant_temp))
                        elif type(cell) == Material:
                            c_ = Material(*cell.get_properties(), pos)
                        newmap[c_.pos[1]][c_.pos[0]] = c_
            l = []

            for r in newmap:
                l.extend(r)
            sim.map = l

        return sim

    def save_json(self, path, map_, mat, settings):
        fixed_size = (1000,600)

        obj = {
            "name":int(time.time()),
            "options":{
                **settings,
                "tick":settings.get('tick', 0.005),
                "cell":settings.get('size', 1),
            },
            "material":mat,
            "body":map_
        }
        if settings.get('upscale', False):
            obj["options"]["upscale"] = settings["upscale"]

        #path = 'map/{}.json'.format(obj["name"]);
        f = open(path, 'w')
        f.write(json.dumps(obj))
        f.close()
        return path
