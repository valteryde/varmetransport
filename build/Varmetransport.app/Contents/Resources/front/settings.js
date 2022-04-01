
function dcopy(v) {
  return JSON.parse(JSON.stringify(v));
}

//https://iconmonstr.com/check-mark-1-svg/
const CHECKMARK = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="white" stroke="white" d="M20.285 2l-11.285 11.567-5.286-5.011-3.714 3.716 9 8.728 15-15.285z"/></svg>';
const ARROW = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>'

var data = {}
function checkbox_toggle(id) {
  var e = document.querySelector('[data-id='+id+']');
  e.children[0].classList.toggle('toggled')
  if (data[id]) {data[id] = false} else {data[id] = true}
  tunnel.update_settings(data);
}

function select_change(id) {
  var e = document.querySelector('[data-id='+id+']').children[1].children[0];
  console.log(e)
  data[id] = [e.selectedIndex, e.children[e.selectedIndex].innerHTML]
  tunnel.update_settings(data);
}

function input_update(e, id) {
  data[id] = e.target.value;
  tunnel.update_settings(data);
}

function set_data(opt) {

  for (const i in opt) {
    var e = document.querySelector('[data-id="'+i+'"]');
    if (!e) {continue}

    if (e.dataset.type == 'checkbox') {
      if (opt[i]) {e.children[0].classList.add('toggled')} else {e.children[0].classList.remove('toggled')}
    } else if (e.dataset.type == 'input') {
      e.children[1].value = opt[i]
    } else if (e.dataset.type == 'multiple') {
      e.children[1].children[0].selectedIndex = opt[i][0]
    }
  }
  data = opt
}

function get_text(e) {
  const ce = e.cloneNode(true); //cloned element
  var offset = 0;
  for (var i = 0; i < ce.children.length+offset; i++) {
    ce.children[i-offset].remove()
    offset++
  }
  var text  = dcopy(ce.innerText)
  delete ce
  return text;
}

function init(qs) {
  var e_ = document.querySelector(qs);
  e_.classList.add('settings-container');
  var sections = e_.children;
  for (var i = 0; i < sections.length; i++) {
    console.log(sections.length)
    sections[i].classList.add('settings-section');
    var elements = sections[i].querySelectorAll('div');
    for (var j = 0; j < elements.length; j++) {
      var e = elements[j];
      if (e.dataset.type == 'checkbox') {
        e.innerHTML = '<button onclick="checkbox_toggle('+"'"+e.dataset.id+"'"+')">'+CHECKMARK+'</button>'+'<p>'+e.innerHTML+'</p>'
      } else if (e.dataset.type == 'multiple') {
        var html = '<p>'+get_text(e)+ '</p>';
        html += '<div class="select-container"> <select onchange="select_change('+ "'" + e.dataset.id + "'" +')">';
        children = e.querySelectorAll('div')
        for (var k = 0; k < children.length; k++) {
          html += '<option>' + children[k].innerHTML + '</option>'
        }
        html += '</select>';
        html += ARROW + '</div>';
        e.innerHTML = html;
      } else if (e.dataset.type == 'input') {
        e.innerHTML = '<p>'+e.innerHTML+'</p><input onkeyup="input_update(event, '+ "'" + e.dataset.id + "'" +')" placeholder="'+e.dataset.placeholder+'" onclick="input_update(event, '+"'"+e.dataset.id+"'"+')"></input>';
      }
    }
  }
}
