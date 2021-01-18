$('#similar_items').on('slide.bs.carousel', function (e) {
  /*
      CC 2.0 License Iatek LLC 2018 - Attribution required
  */
  var $e = $(e.relatedTarget);
  var idx = $e.index();
  var itemsPerSlide = 5;
  var totalItems = $('.carousel-item').length;

  if (idx >= totalItems-(itemsPerSlide-1)) {
      var it = itemsPerSlide - (totalItems - idx);
      for (var i=0; i<it; i++) {
          // append slides to end
          if (e.direction=="left") {
              $('.carousel-item').eq(i).appendTo('.carousel-inner');
          }
          else {
              $('.carousel-item').eq(0).appendTo('.carousel-inner');
          }
      }
  }
});

$('img[data-enlargeable]').addClass('img-enlargeable').click(function(){
  var src = $(this).attr('src');
  var modal;
  function removeModal(){ modal.remove(); $('body').off('keyup.modal-close'); }
  modal = $('<div>').css({
      background: 'RGBA(0,0,0,.5) url('+src+') no-repeat center',
      backgroundSize: 'contain',
      width:'100%', height:'100%',
      position:'fixed',
      zIndex:'10000',
      top:'0', left:'0',
      cursor: 'zoom-out'
  }).click(function(){
      removeModal();
  }).appendTo('body');
  //handling ESC
  $('body').on('keyup.modal-close', function(e){
    if(e.key==='Escape'){ removeModal(); } 
  });
});

$('#more-images-slide').on('slide.bs.carousel', function (e) {
  /*
      CC 2.0 License Iatek LLC 2018 - Attribution required
  */
  var $e = $(e.relatedTarget);
  var idx = $e.index();
  var itemsPerSlide = 1;
  var totalItems = $('.carousel-item').length;

  if (idx >= totalItems-(itemsPerSlide-1)) {
      var it = itemsPerSlide - (totalItems - idx);
      for (var i=0; i<it; i++) {
          // append slides to end
          if (e.direction=="left") {
              $('.carousel-item').eq(i).appendTo('.carousel-inner');
          }
          else {
              $('.carousel-item').eq(0).appendTo('.carousel-inner');
          }
      }
  }
});







// Product Rating

//   const one = document.getElementById('first')
//   const two = document.getElementById('second')
//   const three = document.getElementById('third')
//   const four = document.getElementById('fourth')
//   const five = document.getElementById('fifth')
  
//   const rateForm = document.querySelector('.rate-form')
  
//   const confirmBox = document.getElementById('confirm-box')

//   const handleStarSelect = (size) => {
//     const children = rateForm.children
//     for (let i=0; i<children.length; i++){
//       if(i <= size){
//         children[i].classList.add('checked')
//       } else{
//         children[i].classList.remove('checked')
//       }
//     }
//   }

//   const handleSelect = (selection) => {
//     switch(selection){
//       case 'first': {
//         handleStarSelect(1)
//         return
//       }
//       case 'second': {
//         handleStarSelect(2)
//         return
//       }
//       case 'third': {
//         handleStarSelect(3)
//         return
//       }
//       case 'fourth': {
//         handleStarSelect(4)
//         return
//       }
//       case 'fifth': {
//         handleStarSelect(5)
//         return
//       }
//     }
//   }

//   const getNumericValue = (stringValue) => {
//     let numericVlaue;
//     if(stringValue == 'first'){
//       numericVlaue = 1
//     }else if(stringValue == 'second'){
//       numericVlaue = 2
//     }
//     else if(stringValue == 'third'){
//       numericVlaue = 3
//     }
//     else if(stringValue == 'fourth'){
//       numericVlaue = 4
//     }
//     else if(stringValue == 'fifth'){
//       numericVlaue = 5
//     }
//     else{
//       numericVlaue = 0
//     }
//   }

//   if (one){
//     const arr = [one, two, three, four, five]

//     arr.forEach(item => item.addEventListener('mouseover', (event) => {
//       handleSelect(event.target.id)
//     }))

//     arr.forEach(item => item.addEventListener('click', (event) => {
//       const val = event.target.id

//       let isSubmit = false
//       rateForm.addEventListener('submit', e => {
//         const csrf = document.getElementsByName('csrfmiddlewaretoken')
//         e.preventDefault()
//         if (isSubmit){
//           return
//         }
//         isSubmit = true
//         const id = e.target.id
//         const val_num = getNumericValue(val)
//         console.log(csrf)
//         console.log(csrf[0].value)

//         $.ajax({
//           type: 'POST',
//           url: "{% url 'product:rate-product' %}",
//           data: {
//             'csrfmiddlewaretoken': csrf[0].value,
//             'el_id': id,
//             'val': val_num,
//           },
//           success: function(response){
//             console.log(response)
//             confirmBox.innerHTML = `<h1>Sucessfully rated</h1>`
//           },
//           error: function(error){
//             console.log(error)
//             confirmBox.innerHTML = `<h1>Something went wrong</h1>`
//           },
//         })
//       })
//     }))
//   }



// //Similar Product Recommendation

// $('.carousel.carousel-multi-item.v-2 .carousel-item').each(function () {
//     var next = $(this).next();
//     if (!next.length) {
//       next = $(this).siblings(':first');
//     }
//     next.children(':first-child').clone().appendTo($(this));
  
//     for (var i = 0; i < 4; i++) {
//       next = next.next();
//       if (!next.length) {
//         next = $(this).siblings(':first');
//       }
//       next.children(':first-child').clone().appendTo($(this));
//     }
//   });