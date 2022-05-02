
  $(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('ul.tabs').tabs();
    $('#file-upload').bind('change', function() { var fileName = ''; fileName = $(this).val(); $('#file-selected').html(fileName).css("visibility", "visible");; })
    $('.collapsible').collapsible();
    $(".dropdown-trigger").dropdown();
    $(".dropdown-trigger-side").dropdown();
    $('input#input_text, textarea#project-description').characterCounter();
  });
 
      

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.fixed-action-btn');
  var instances = M.FloatingActionButton.init(elems, {
    direction: 'left'
  });
});
    



