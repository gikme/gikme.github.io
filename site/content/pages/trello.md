Title: Списки тем
Author: gikme  
Tags: tools, podcast, support, theme  
Slug: trello  
Order: 99
Nocomment: 1


<div class="trello-ui" id="trelloUI">
    <div class="trello-ui__user-info"></div>
    <div class="trello-ui__content"></div>
    <div class="trello-ui__message"></div>
</div>

* Букмарклет для добавления тем: <a href="javascript:(function(win%2Cname%2Cdesc)%7Bwin.open('https%3A%2F%2Ftrello.com%2Fadd-card'%2B'%3Fsource%3D'%2Bwin.location.host%2B'%26mode%3Dpopup'%2B'%26url%3D'%2BencodeURIComponent(win.location.href)%2B'%26name%3D'%2BencodeURIComponent(document.title)%2B'%26desc%3D'%2BencodeURIComponent(name)%2BencodeURIComponent('%20%20%5Cn')%2BencodeURIComponent(win.location.href)%2B'%26idList%3D556594c8dd3cea1107c4b13e'%2C'add-trello-card'%2C'width%3D500%2Cheight%3D600%2Cleft%3D'%2B(win.screenX%2B(win.outerWidth-500)%2F2)%2B'%2Ctop%3D'%2B(win.screenY%2B(win.outerHeight-740)%2F2))%7D)(window%2Cdocument.title%2CgetSelection%3FgetSelection().toString()%3A'')">+тема</a>
![Trello Bookmarklet]({filename}/images/tools/trello-bookmarklet.png)

Исходник букмарклета:

    :::html
    <a href="javascript:(function(win%2Cname%2Cdesc)%7Bwin.open('https%3A%2F%2Ftrello.com%2Fadd-card'%2B'%3Fsource%3D'%2Bwin.location.host%2B'%26mode%3Dpopup'%2B'%26url%3D'%2BencodeURIComponent(win.location.href)%2B'%26name%3D'%2BencodeURIComponent(document.title)%2B'%26desc%3D'%2BencodeURIComponent(name)%2BencodeURIComponent('%20%20%5Cn')%2BencodeURIComponent(win.location.href)%2B'%26idList%3D56a7123d81adfc99f8fe8b22'%2C'add-trello-card'%2C'width%3D500%2Cheight%3D600%2Cleft%3D'%2B(win.screenX%2B(win.outerWidth-500)%2F2)%2B'%2Ctop%3D'%2B(win.screenY%2B(win.outerHeight-740)%2F2))%7D)(window%2Cdocument.title%2CgetSelection%3FgetSelection().toString()%3A'')">+gik.me</a>