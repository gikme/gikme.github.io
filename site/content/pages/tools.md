Title: Полезняк  
Author: gikme  
Tags: tools, podcast, support, theme  
Slug: tools  
Order: 99


Чтобы быстро добавть тему перетащи ссылку на панел закладок и кликни по ней на странице новости:

<a href="javascript:(function(win%2Cname%2Cdesc)%7Bwin.open('https%3A%2F%2Ftrello.com%2Fadd-card'%2B'%3Fsource%3D'%2Bwin.location.host%2B'%26mode%3Dpopup'%2B'%26url%3D'%2BencodeURIComponent(win.location.href)%2B'%26name%3D'%2BencodeURIComponent(document.title)%2B'%26desc%3D'%2BencodeURIComponent(name)%2BencodeURIComponent('%20%20%5Cn')%2BencodeURIComponent(win.location.href)%2B'%26idList%3D556594c8dd3cea1107c4b13e'%2C'add-trello-card'%2C'width%3D500%2Cheight%3D600%2Cleft%3D'%2B(win.screenX%2B(win.outerWidth-500)%2F2)%2B'%2Ctop%3D'%2B(win.screenY%2B(win.outerHeight-740)%2F2))%7D)(window%2Cdocument.title%2CgetSelection%3FgetSelection().toString()%3A'')">+тема</a>

![Trello Bookmarklet]({filename}/images/tools/trello-bookmarklet.png)

Исходник букмарклета:

    javascript:(function(win,name,desc){win.open('https://trello.com/add-card'+'?source='+win.location.host+'&mode=popup'+'&url='+encodeURIComponent(win.location.href)+'&name='+encodeURIComponent(document.title)+'&desc='+encodeURIComponent(name)+encodeURIComponent('  \n')+encodeURIComponent(win.location.href)+'&idList=556594c8dd3cea1107c4b13e','add-trello-card','width=500,height=600,left='+(win.screenX+(win.outerWidth-500)/2)+',top='+(win.screenY+(win.outerHeight-740)/2))})(window,document.title,getSelection?getSelection().toString():'')
