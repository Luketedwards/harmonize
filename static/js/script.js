
  $(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
  });


 
// Script for password confirmation


document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.fixed-action-btn');
  var instances = M.FloatingActionButton.init(elems, {
    direction: 'left'
  });
});
    
$(document).ready(function(){
  // TABS
  $('ul.tabs').tabs();
});

$(document).ready(function(){
  $('#file-upload').bind('change', function() { var fileName = ''; fileName = $(this).val(); $('#file-selected').html(fileName).css("visibility", "visible");; })
});

