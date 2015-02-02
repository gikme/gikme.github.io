'use strict';

$( function(){
  $( '.article__content img' ).each(function(){
    var $this = $(this);
    $this.wrap('<a href="' + $this.attr('src') + '" rel="lightbox"></a>');
  });

  $('[rel="lightbox"]').fluidbox();

  var showVK = function(){

    VK.Widgets.Group(
      "vk_groups",
      {
        mode: 2,
        width: 220,
        height: 400,
        color1: 'FFFFFF',
        color2: '2B587A',
        color3: '5B7FA6'
      },
      48255349
    );
  }

  showVK();
});
