'use strict';

(function($){
  var defaultMessageClass = 'trello-ui__message';
  var defaultBoardId = '513450d203b5695561002bfd';
  var UI = $('#trelloUI');
  var messageUI = UI.find('.' + defaultMessageClass);
  var contentUI = UI.find('.trello-ui__content');
  var userInfoUI = UI.find('.trello-ui__user-info');
  var user, lists;
  var authButton = userInfoUI.find('.trello-ui__login');

  if (typeof localStorage != 'undefined'){
    var token = localStorage.getItem('trello_token');

    if (token){
      Trello.setToken(token);
    }
  }

  var getAuthButton = function(){
    // authButton = userInfoUI.find('.trello-ui__login');

    if (authButton.length === 0){
      authButton = $('<button type="button" class="header__menu-item header__menu-item_donate trello-ui__login">Войти в Trello</button>').on('click', function(){
        trelloLogin(true);
      });
    }

    return authButton;
  };

  var showMessage = function(message, status){
    messageUI.empty();
    var messageClass = defaultMessageClass;

    if (status){
      messageClass += ' ' + defaultMessageClass + '_status_' + status;
    }

    messageUI.attr('class', messageClass);
    messageUI.html(message);

    setTimeout(clearMessage, 3000);
  };

  var clearMessage = function(){
    messageUI.empty();
    messageUI.attr('class', defaultMessageClass);
  };

  var authenticationSuccess = function(success){
    UI.text(success);
    authButton.hide();
    getUserInfo();
  };

  var authenticationError = function(error){
    UI.text(error);
    console.error(error);
  };

  var clearSuffixes = function(text, suffixes){
    for (var i in suffixes){
      var parts = text.split(suffixes[i]);

      if (parts.length==2 && parts[1] === ''){
        text = parts[0];
      }
    }

    return text;
  };

  var clearPrefixes = function(text, prefixes){
    for (var i in prefixes){
      var parts = text.split(prefixes[i]);

      if (parts.length==2 && parts[0] === ''){
        text = parts[1];
      }
    }

    return text;
  };

  var clearDoamins = function(url){
    var replacements = [
      ['m.geektimes.ru', 'geektimes.ru']
    ];

    for (var i in replacements){
      url = url.replace(replacements[i][0], replacements[i][1])
    }
    return url;
  };

  var clearUrl = function(url){
    var suffixes = [
      '?from=rss',
      '?from=club',
      '?feed',
      '?utm_source=thematic1',
      '?from=relap'
    ];

    return clearSuffixes(clearDoamins(url.trim()), suffixes).trim();
  };

  var clearText = function(text){
    var suffixes = [
      ' / Geektimes',
      ' | n1.by',
      ' - 4PDA',,
      ': Техника: Наука и техника: Lenta.ru',
      ': Наука и техника: Lenta.ru',
      ': Lenta.ru',
      ' / Мегамозг',
      ' – Журнал «Нож»',
      ' — Meduza',
      ' | RUBLACKLIST.NET',
      ' → Roem.ru',
      ' - YouTube',
      ' / Хабрахабр',
      ' – Афиша Daily',
      ' | ZDNet',
      ' | AppTractor',
      ' | Мел',
      ' :: Общество :: РБК',
      ' | РОСКОМСВОБОДА',
      ' / Блог компании Pult.ru'
    ];

    var prefixes = [
      'Компания Яндекс — Главные новости — ',
      'Ferra.ru - ',
      'TNW: ',
      'TJ: ',
      'OpenNews: ',
      'Фото: ',
      'Технологии | ',
      'ТАСС: Общество - '
    ];

    return clearSuffixes(clearPrefixes(text.trim(), prefixes), suffixes).trim();
  };

  var clearParts = function(parts){
    return [clearText(parts[0]), clearUrl(parts[1])];
  };

  var loadListContent = function(element, target){
    Trello.lists.get(
      $(element).data('id')+'/cards/open',
      function(success){
        var text = '';
        var markdown = $('.markdown_switch').prop("checked");

        for (var i in success){
          var part = '';
          var slices = success[i].desc.split(/\s(?=http)/ig);
          var parts = slices.slice();

          if (parts[0].indexOf('http') > -1){
            parts = [success[i].name, parts[0]];
          }else if (parts.length < 2){
            parts = [success[i].name, ''];
          }

          if (parts[0].indexOf('http') > -1){
            parts = ['⚠ Будь проклят WebView!!!11 😡😡😡 ⚠', parts[0]];
          }

          parts = clearParts(parts);

          if (parts[1]){
            if (markdown){
              part = '[' + parts[0] + '](' + parts[1] + ')';
            }else{
              part = parts.join('  \n');
            }

            if (slices.length > 2){
              for (var i=2; i < slices.length; i++){
                if (markdown){
                  parts[i] = '<' + slices[i] + '>';
                }else{
                  parts[i] = '' + slices[i];
                }

                part += '  \n' + parts[i];
              }
            }
          }else{
            part = parts[0];
          }

          part += '\n\n';
          text += part;
        }


        target.text(text);
        target.show().focus();
      },
      function(error){
        showMessage('Ошибка загрузки списка', 'error');
        console.error(error);
      }
    );
  };

  var showLists = function(){
    var listsUI = contentUI.find('.trello-ui__lists');



    if (!listsUI.length){
      listsUI = $('<div class="trello-ui__lists"><div class="trello-ui__lists-buttons"></div><label><input type="checkbox" class="markdown_switch"/> markdown</label><textarea class="trello-ui__list-content" readonly></textarea></div>');
      contentUI.append(listsUI);
    }

    var listButtonsUI = listsUI.find('.trello-ui__lists-buttons');
    listButtonsUI.empty();
    var listContentUI = listsUI.find('.trello-ui__list-content');
    listContentUI.hide().empty().on('focus', function(){
      this.select();
    });
    var currentList;

    $('.markdown_switch').on('change', function(){
      if (currentList){
        loadListContent(currentList, listContentUI);
      }
    });

    for (var i in lists){
      var list = lists[i];
      var listButton = $(
        '<button type="button" data-id="'
        +list.id
        +'" class="trello-ui__lists-button header__menu-item header__menu-item_talk">'
        +list.name
        +'</button>')
        .on('click', function(){
          currentList = this;
          loadListContent(this, listContentUI);
        });
      listButtonsUI.append(listButton);
    }
  };

  var loadData = function(){
    userInfoUI.append('<img class="trello-ui__avatar" alt="" src="http://www.gravatar.com/avatar/'
      +user.gravatarHash
      +'"/>');
    var logoutButton = $('<button type="button" class="header__menu-item header__menu-item_donate trello-ui__logout">Выйти из Trello</button>').on('click', trelloLogout);

    userInfoUI.append(logoutButton);

    Trello.boards.get(
      defaultBoardId + '/lists/open',
      function(success){
        lists = success;
        showLists();
      },
      function(error){
        showMessage('Ошибка загрузки борды', 'error');
        console.error(error);
      }
    );
  };

  var trelloLogin = function(interactive){
    Trello.authorize({
      type: 'popup',
      name: 'gik.me',
      persist: true,
      interactive: !!interactive,
      scope: {
        read: true,
        write: true
      },
      expiration: 'never',
      success: authenticationSuccess,
      error: authenticationError
    });
  };

  var trelloLogout = function(){
    Trello.deauthorize();
    init();
    authButton.show();
  };

  var getUserInfo = function(){
    Trello.members.get(
      'me',
      function(success){
        user = success;
        loadData();
      },
      function(error){
        console.error('error', error);
        showMessage('Необходимо войти в Trello', 'error');
        authButton.show();
      }
    );
  };

  var init = function(){
    user = undefined;
    lists = undefined;
    contentUI.empty();
    userInfoUI.empty();
    userInfoUI.append(getAuthButton());
    authButton.hide();
  };

  init();
  getUserInfo();
})(jQuery);
