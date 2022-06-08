
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
      $('#about-the-project').addClass('center')
      $('#instruments-and-genre').addClass('center')
      $('#about-the-project').removeClass('left')
      $('#instruments-and-genre').removeClass('right')
    }else{
      $('#about-the-project').removeClass('center')
      $('#instruments-and-genre').removeClass('center')
      $('#about-the-project').addClass('left')
      $('#instruments-and-genre').addClass('right')
    }
  });

  $(window).resize(function(){
    if(window.innerWidth < 1000){
      $('#about-the-project').addClass('center')
      $('#instruments-and-genre').addClass('center')
     
    }else{
      $('#about-the-project').removeClass('center')
      $('#instruments-and-genre').removeClass('center')
      $('#about-the-project').addClass('left')
      $('#instruments-and-genre').addClass('right')
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

  