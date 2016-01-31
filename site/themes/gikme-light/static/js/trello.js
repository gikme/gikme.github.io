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

  var loadListContent = function(element, target){
    Trello.lists.get(
      $(element).data('id')+'/cards/open',
      function(success){
        var text = '';

        for (var i in success){
          var part = success[i].desc.split(/\s(?=http)/ig).join('  \n').trim() + '\n\n';

          if (part.indexOf('http') === 0){
            part = success[i].name + '  \n' + part;
          }

          text += part;
        }

        text = text.replace('m.geektimes.ru', 'geektimes.ru');
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
      listsUI = $('<div class="trello-ui__lists"><div class="trello-ui__lists-buttons"></div><textarea class="trello-ui__list-content" readonly></textarea></div>');
      contentUI.append(listsUI);
    }

    var listButtonsUI = listsUI.find('.trello-ui__lists-buttons');
    listButtonsUI.empty();
    var listContentUI = listsUI.find('.trello-ui__list-content');
    listContentUI.hide().empty().on('focus', function(){
      this.select();
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
  }

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
})(jQuery)
