
  $(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('ul.tabs').tabs();
    $('#file-upload').bind('change', function() { var fileName = ''; fileName = $(this).val(); $('#file-selected').html(fileName).css("visibility", "visible");; })
    $('.collapsible').collapsible();
    $(".dropdown-trigger").dropdown();
    $(".dropdown-trigger-side").dropdown();
    $('input#input_text, textarea#project-description').characterCounter();
    $('.modal').modal();
    if(window.innerWidth < 1000){
      $('#bio-container').removeClass('container');
      $('#about-the-project').addClass('center')
      $('#instruments-and-genre').addClass('center')
      
    }
  });

  $(window).resize(function(){
    if(window.innerWidth < 1000){
      $('#bio-container').removeClass('container');
     
    }else{
      $('#bio-container').addClass('container');
     
    }
    
  });
  $(window).resize(function(){
    if(window.innerWidth < 600){
      
      $('.about-the-project').addClass('center')
      $('.instruments-and-genre').addClass('center')
    }else{
     
      $('.about-the-project').removeClass('center')
      $('.instruments-and-genre').removeClass('center')
    }
    
  });
  

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.fixed-action-btn');
  var instances = M.FloatingActionButton.init(elems, {
    direction: 'left'
  });
});


    



