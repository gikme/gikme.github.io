'use strict';

$( function(){
  audiojs.events.ready(function() {
    var as = audiojs.createAll({initialVolume: 1});

    if (window.isPodcast){
      $('.article__content p').each(function(){
        var $this = $(this);
        var html = $this.html().replace(/(\d+:\d+(?::\d+)*)/ig, '<span class="audio-rewind">$1</span>');
        $this.html(html);
      });

      var rewinder;

      var trySkip = function(audio, percent, timeout){
        var timeout = timeout || 500;

        if (audio.loadedPercent >= percent){
          audio.skipTo(percent);
          audio.play();

          return;
        }

        if (rewinder){
          clearTimeout(rewinder);
        }

        rewinder = setTimeout(function(){
          trySkip(audio, percent, timeout+100)
        }, timeout);

        return;
      }

      var rewind = function(audio, time){
        if (!time || !audio){
          return;
        }

        if (rewinder){
          clearTimeout(rewinder);
        }

        audio.playPause();
        audio.pause();

        var parts = time.split(':');
        var targetTime = 0;

        for (var i=0; i<=parts.length; i++){
          var part = parts.pop();

          if (!i){
            targetTime += parseInt(part, 10);
          }else if(i == 1){
            targetTime += parseInt(part, 10) * 60;
          }else{
            targetTime += parseInt(part, 10) * 60 * 60;
          }
        }

        var percent = targetTime / audio.duration;

        trySkip(audio, percent);
      }

      $('.audio-rewind').on('click', function(){
        var $this = $(this);
        rewind(as[0], $this.text());
        return false;
      });
    }
  });

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
