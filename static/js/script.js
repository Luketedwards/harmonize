
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
      
    }
  });

  $(window).resize(function(){
    if(window.innerWidth < 1000){
      
     
    }else{
      
     
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

$(document).ready(function(){
var password = document.getElementById("password")
  , confirm_password = document.getElementById("passwordConfirm");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
  } else {
    confirm_password.setCustomValidity('');
  }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
});    



