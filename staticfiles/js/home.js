$(document).on('submit', '#subscribe_newsletter_form', function(e){
    e.preventDefault(); // prevents the page from getting refreshed
    //now we write our ajax code
    $.ajax({
        type: 'POST',
        url: "{% url 'customer:subscribe_newsletter' %}",
        data:{
            user_email:$('#newsletter_email').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
            document.getElementById("newsletter_email").value = '';
            swal("Subscribed to the Newsletter!", {
              icon: 'success',
              buttons: false,
              timer: 1000,
            });
        },
        error: function() {
          document.getElementById("newsletter_email").value = '';
          swal("Could not subscribe to the Newsletter!", {
              icon: 'error',
              buttons: false,
              timer: 1000,
            });
        }
    });
  });