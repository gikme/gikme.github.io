'use strict';

var showVK = function(){
  var width, height, windowWidth = window.innerWidth;

  if (windowWidth < 1200){
    if (windowWidth < 600){
      width = 250;
      height = 250;
    }else{
      width = 600;
      height = 250;
    }
  }else{
    width = 250;
    height = 600;
  }

  document.getElementById('vk_groups').innerHTML = '';

  VK.Widgets.Group(
    "vk_groups",
    {
      mode: 2,
      // wide: 1,
      width: width,
      height: height,
      color1: 'FFFFFF',
      color2: '2B587A',
      color3: '5B7FA6'
    },
    48255349
  );
}

showVK();
window.onresize = showVK;
