// $(document).on('submit', '#add_to_cart', function(e){
//     e.preventDefault();

//     $.ajax({
//         type: 'POST',
//         url: "{% url 'carts:update' %}",
//         data: {
//             qty: $('qty'),
//             product_id: $('product_id'),
//         },
//         header: {'X-CSRFToken': '% csrf_token %'},
//     });
// });