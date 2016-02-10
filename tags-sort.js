(function(){
  var length = 22;
  var items = [];
  
  $('.post.archives li').each(function(){
    var item = $(this).text().split(' (');

    item[1] = parseInt(item[1].slice(0,-1));
    items.push({name:item[0],count:item[1]});
  });

  items.sort(function(a, b){
    return b.count-a.count;
  });
  
  console.log('#'+items.slice(0,length).map(function(item){return item.name.replace(' ', '_') + ' [' + item.count + ']'}).join(', #'));
console.log('#'+items.slice(0,length).map(function(item){return item.name.replace(' ', '_')}).join(', #'));
})();
