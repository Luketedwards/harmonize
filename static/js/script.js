
  $(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
  });

// Script for password confirmation

$("#password").on("focusout", function (e) {
  if ($(this).val() != $("#passwordConfirm").val()) {
      $("#passwordConfirm").removeClass("valid").addClass("invalid");
  } else {
      $("#passwordConfirm").removeClass("invalid").addClass("valid");
  }
});

$("#passwordConfirm").on("keyup", function (e) {
  if ($("#password").val() != $(this).val()) {
      $(this).removeClass("valid").addClass("invalid");
  } else {
      $(this).removeClass("invalid").addClass("valid");
  }
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.fixed-action-btn');
  var instances = M.FloatingActionButton.init(elems, {
    direction: 'left'
  });
});
    
