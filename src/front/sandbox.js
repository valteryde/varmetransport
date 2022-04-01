
const gradient = [
  "rgb(250, 180, 1)",
  "rgb(246, 167, 1)",
  "rgb(241, 153, 2)",
  "rgb(236, 140, 2)",
  "rgb(232, 127, 3)",
  "rgb(227, 114, 3)",
  "rgb(223, 101, 4)",
  "rgb(218, 87, 5)",
  "rgb(213, 74, 5)",
  "rgb(209, 61, 6)",
  "rgb(204, 48, 6)",
  "rgb(199, 34, 7)",
  "rgb(195, 21, 7)",
  "rgb(190, 8, 8)"
]
const a = 0;
const b = 50;
function get_heater_color(val) {
  if (val >= b) {
    return gradient[gradient.length-1]
  } else if (val <= a) {
    return gradient[0]
  }
  return gradient[Math.round(((val - a) / b) * (gradient.length-1))]
}

function dcopy(v) {
  return JSON.parse(JSON.stringify(v));
}

function reset(c) {
  c.fillStyle = 'transparent';
  c.strokeStyle = 'transparent'
}

function rect(c, color, rect) {
  var ctx = c.getContext('2d');
  ctx.fillStyle = color
  ctx.fillRect(...rect);
  reset(c);
}

function line(c, color, p1, p2) {
  var ctx = c.getContext('2d');
  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = color;
  ctx.moveTo(...p1);
  ctx.lineTo(...p2);
  ctx.closePath();
  ctx.stroke();
  reset(ctx);
}

var changed = false;
window.onresize = () => {
  changed = true;
}


var _sandbox_;
function loop() {
  if (changed) {
    changed = false;
    var style = getComputedStyle(document.querySelector('canvas'));
    _sandbox_.width = style.width.replace('px', '');
    _sandbox_.height = style.height.replace('px', '');
  }

  try {
    _sandbox_.draw();
  } catch (error) {
    console.error(error);
  }
  window.requestAnimationFrame(loop);
}

class Sandbox {
  constructor(selector, grid, background='lightgrey') {
    this.canvas = document.querySelector(selector);
    this.grid = grid;
    this.reset_map(grid);

    this.size = [1000,1000];
    this.canvas.width = dcopy(this.size[0]);
    this.canvas.height = dcopy(this.size[1]);
    var style = window.getComputedStyle(this.canvas)
    this.width = parseFloat(style.width.replace('px', ''));
    this.height = parseFloat(style.height.replace('px', ''));
    this.left = 7;
    this.top = 55;
    this.ma = {
      0:{"type":"air", "color":"transparent"},
      1:{"type":"concrete", "lambda":1.8, "heatcapacity":1.1, "density":2400, "color":"rgb(100,100,100)"},
      2:{"type":"tree", "lambda":0.18, "heatcapacity":1.5, "density":700, "color":"rgb(7,255,50)"}, /* bøg */
      3:{"type":"glass", "lambda":1.05, "heatcapacity":0.84, "density":2500, "color":"rgb(255,255,255)"},
      4:{"type":"metal", "lambda":174, "heatcapacity":0.9, "density":2700, "color":"rgb(10,10,10)"}, /* aluminium */
      5:{"type":"isolater", "lambda":0, "heatcapacity":0, "density":0, "color":"rgb(255,255,50)"}, /* aluminium */
      6:{"type":"MDF", "lambda":0.18, "heatcapacity":1.7, "density":800, "color":"rgb(7,255,50)"}, /* MDF */

    };
    this.count = Object.keys(this.ma).length + 100;
    this.mousepos = [0,0];
    this.background = background;
    this.preview = {"m":undefined, "p1":undefined, "p2":undefined};
    this.canvas.onmousemove = e=> {
      this.preview["p2"] = e;
      this.mousepos = this.fix_pos_to_grid(e);
    }

    this.mousedown = false;
    this.canvas.onmousedown =e=> {
      this.preview["m"] = dcopy(this.drawing_material);
      this.preview["p1"] = e;
    }
    this.draw_map();
    this.canvas.onmouseup =e=> {
      this.freeze_preview();
    }
    this.drawing_material = 0;

    setTimeout(function () {
      tunnel.get_map().then(r=>{

        _sandbox_.map = r[0];
        _sandbox_.ma = Object.assign(r[1], _sandbox_.ma);

      })
    }, 500);


    _sandbox_ = this;
    window.requestAnimationFrame(loop)

  }

  draw() {
    //background
    rect(this.canvas, this.background, [0, 0, this.size[0], this.size[1]]);
    this.draw_map();
    this.line_highlight();
  }


  reset_map(grid) {
    this.map = []

    for (var i = 0; i < grid[1]; i++) {
      this.map.push([]);

      for (var j = 0; j < grid[0]; j++) {
        this.map[i].push(0);
      }
    }
  }

  set(m) {
    this.drawing_material = m
  }


  line_highlight(e) {
    var p = this.mousepos;

    //y
    line(this.canvas, 'rgba(255,0,0,.5)', [0, p[1]/this.grid[1]*this.size[1]], [this.size[0], p[1]/this.grid[1]*this.size[1]]);
    line(this.canvas, 'rgba(255,0,0,.5)', [0, (p[1]+1)/this.grid[1]*this.size[1]], [this.size[0], (p[1]+1)/this.grid[1]*this.size[1]]);

    //x
    line(this.canvas, 'rgba(255,0,0,.5)', [p[0]/this.grid[0]*this.size[0], 0], [p[0]/this.grid[0]*this.size[0], this.size[1]])
    line(this.canvas, 'rgba(255,0,0,.5)', [(p[0]+1)/this.grid[0]*this.size[0], 0], [(p[0]+1)/this.grid[0]*this.size[0], this.size[1]])


    //box for show
    this.draw_box(...p, 'rgba(255,0,0,.1)')
  }

  freeze_preview() {

    var cells = this.get_preview_cells();
    for (var i = 0; i < cells.length; i++) {
      this.create_box_by_pos(...cells[i]);
    }

    this.preview = {}
  }

  fix_pos_to_grid(e) {
    if (!e) return

    var x = (e.x-this.left)/this.width;
    var y = (e.y-this.top)/this.height;
    var gx = Math.floor(x*this.grid[0]);
    var gy = Math.floor(y*this.grid[1]);
    return [gx, gy];
  }

  create_box_by_event(e) {
    var pos = this.fix_pos_to_grid(e);
    this.map[pos[1]][pos[0]] = dcopy(this.drawing_material);
  }

  create_box_by_pos(x,y) {
    this.map[y][x] = dcopy(this.drawing_material);
  }

  get_preview_cells() {
    var p1 = this.fix_pos_to_grid(this.preview["p1"])
    var p2 = this.fix_pos_to_grid(this.preview["p2"])
    var cells = [p1];
    var _a = [
      Math.abs(p2[0]-p1[0]),
      Math.abs(p2[1]-p1[1])
    ]
    var dir = 1-_a.indexOf(Math.min(..._a))
    var l = Math.max(p1[dir], p2[dir]) //large
    var s = Math.min(p1[dir], p2[dir]) //small

    if (_a[0] > _a[1]) {

      for (var i = s+1; i < l; i++) {
        cells.push([i,p1[1]])
      }
      cells.push([p2[0], p1[1]])

    } else {

      for (var i = s+1; i < l; i++) {
        cells.push([p1[0],i])
      }
      cells.push([p1[0], p2[1]])
    }

    return cells
  }

  draw_map() {

    //draw cells
    for (var i = 0; i < this.grid[1]; i++) {

      for (var j = 0; j < this.grid[0]; j++) {

        if (this.map[i][j] != 0) {
          this.draw_box(j, i, this.ma[this.map[i][j]].color);
        }

      }
    }

    //draw preview
    if (this.preview["p1"]){
      var cells = this.get_preview_cells()
      for (var i = 0; i < cells.length; i++) {
        this.draw_box(...cells[i], this.ma[this.drawing_material].color);
      }
    }

    //draw lines
    for (var i = 1; i < this.grid[1]; i++) {
      line(this.canvas, 'rgba(50,50,50,.2)', [0, i/this.grid[1]*this.size[1]], [this.size[0], i/this.grid[1]*this.size[1]]);
    }
    for (var i = 1; i < this.grid[0]; i++) {
      line(this.canvas, 'rgba(50,50,50,.2)', [i/this.grid[0]*this.size[0], 0], [i/this.grid[0]*this.size[0], this.size[1]])
    }

  }

  draw_box(x,y,color) {
    rect(this.canvas, color, [x*this.size[0]/this.grid[0],y*this.size[1]/this.grid[1],this.size[0]/this.grid[0],this.size[1]/this.grid[1]]);
  }

  upload() {
    return tunnel.save(this.map, this.ma);
  }

  heater_constant() {
    bootbox.prompt("Konstant temperatur, fx. en radiator ([T] = Celcius)", function(res){
      if (res) {
        _sandbox_.count++
        _sandbox_.ma[_sandbox_.count] = {"type":"heater", "value":parseFloat(res), 'color':get_heater_color(parseFloat(res))}
        _sandbox_.set(_sandbox_.count)
      }
    });
  }

  heater_one() {
    bootbox.prompt("Enkelt temperatur ([T] = Celcius)", function(res){
      if (res) {
        _sandbox_.count++
        _sandbox_.ma[_sandbox_.count] = {"type":"warmth", "value":parseFloat(res), 'color':'rgb(255,0,100)'}
        _sandbox_.set(_sandbox_.count)
      }
    });
  }

}
