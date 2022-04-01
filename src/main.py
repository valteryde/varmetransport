
# *** LIBS ***
from bird import Bird, render_html, get_style, Server, BaseApi, PID
from simulation import *
import multiprocessing
import requests
import json
from loader import Loader
import os

bird = Bird("Termospace", browser=False)
basedir = os.path.abspath(os.path.sep.join(os.path.split(__file__)[:-1]))
serv = Server(os.path.join(os.path.join(basedir, 'front')))
settings_path = os.path.join(basedir,'settings.json')
basedir_sim[0] = basedir

# *** ROUTES ***
@bird.route
def index():
    return render_html(os.path.join(basedir,'front','index.html')), get_style(os.path.join(basedir,'front','master.css'))

@bird.route
def setting():
    f = open(os.path.join(basedir, 'settings.json'),'r')
    set = f.read()
    f.close()
    return render_html(os.path.join(basedir, 'front', 'setting.html'),settings=set.replace('\n', '')), get_style(os.path.join(basedir,'front', 'setting.css'))


# *** functions for multiprocessing unit ***
def loader(p):
    if not requests.get('http://localhost:5000/_proc_/{}'.format(p)):
        return False
    return True
def f1(m):
    Loader().load_json(m).loop_animation()
def f2(m,i):
    Loader().load_json(m).simulation_static(iterations=i, progress=loader)
def f3(m,t):
    Loader().load_json(m).simulation_static(timer=t, progress=loader)
def f4(m):
    Loader().load_json(m).loop_animation_under_layer()


stop = False
@serv.server.route('/_proc_/<string:p>')
def _proc_(p):
    global stop
    bird.evaluate_js('loader({})'.format(p))
    if stop:
        stop = False
        return '', 400
    return '', 200


# *** API ***
processes = []
class Api(BaseApi):
    """docstring for Api."""

    def __init__(self):
        super(BaseApi, self).__init__()
        self.__render__()
        self.filepath = os.path.join(basedir,'map','live.json')
        self.settings = json.loads(open(settings_path, 'r').read())

    def run(self, t, val=0):
        val = int(val)
        map_ = self.filepath
        print(self.filepath)
        for p in processes:
            print('Killed: ', p)
            p.kill()
        p = []
        
        try:
            if t == 'animate':
                p = multiprocessing.Process(name='p', target=f1, args=(map_,))
            elif t == 'static_iterations':
                p = multiprocessing.Process(name='p', target=f2, args=(map_,val))
            elif t == 'static_timer':
                p = multiprocessing.Process(name='p', target=f3, args=(map_,val))
            elif t == 'animate_under':
                p = multiprocessing.Process(name='p', target=f4, args=(map_,))
            processes.append(p)
            p.start()
        except Exception as e:
            print(str(e))

    def stop(self):
        global stop
        stop = True

    def save(self, map_, mat):
        self.filepath = Loader().save_json(self.filepath, map_, mat, self.settings)

    def update_settings(self, settings):
        f = open(settings_path,'r')
        r = f.read()
        f.close()
        if len(r) > 0:
            set = json.loads(r)
        else:
            set = {}
        res = settings.get("cellsize")
        if res:
            settings["size"] = int(list(map(int,res[1].split('x')))[0]) / 50
        self.settings = {**set,**settings}
        f = open(settings_path, 'w')

        if not self.settings.get("restoggle", True):
            self.settings["upscale"] = ''

        f.write(json.dumps(self.settings))
        f.close()


    def get_map(self):
        j = json.loads(open(os.path.join(basedir, 'map', 'live.json'), 'r').read())
        return [j["body"], j["material"]]


# *** MAIN ***
if __name__ == '__main__':
    # new thread
    serv.run()

    # main thread
    bird.run(debug=True, api=Api())

    # close all
    for p in processes:
        print('Killed: ', p)
        p.kill()

    print("\033[04m\033[92mProgram closed succesfully\033[00m")
    os.kill(PID, 9) #knock out
