let featuedImg = document.getElementById('featured-image');
// let smallImgs = document.getElementsByClassName('small-Img');

// smallImgs[0].addEventListener('click', () => {
//     featuedImg.src = smallImgs[0].src;
//     smallImgs[0].classList.add('sm-card')
//     smallImgs[1].classList.remove('sm-card')
//     smallImgs[2].classList.remove('sm-card')
//     smallImgs[3].classList.remove('sm-card')
//     smallImgs[4].classList.remove('sm-card')
// })
// smallImgs[1].addEventListener('click', () => {
//     featuedImg.src = smallImgs[1].src;
//     smallImgs[0].classList.remove('sm-card')
//     smallImgs[1].classList.add('sm-card')
//     smallImgs[2].classList.remove('sm-card')
//     smallImgs[3].classList.remove('sm-card')
//     smallImgs[4].classList.remove('sm-card')
// })
// smallImgs[2].addEventListener('click', () => {
//     featuedImg.src = smallImgs[2].src;
//     smallImgs[0].classList.remove('sm-card')
//     smallImgs[1].classList.remove('sm-card')
//     smallImgs[2].classList.add('sm-card')
//     smallImgs[3].classList.remove('sm-card')
//     smallImgs[4].classList.remove('sm-card')
// })
// smallImgs[3].addEventListener('click', () => {
//     featuedImg.src = smallImgs[3].src;
//     smallImgs[0].classList.remove('sm-card')
//     smallImgs[1].classList.remove('sm-card')
//     smallImgs[2].classList.remove('sm-card')
//     smallImgs[3].classList.add('sm-card')
//     smallImgs[4].classList.remove('sm-card')
// })
// smallImgs[4].addEventListener('click', () => {
//     featuedImg.src = smallImgs[4].src;
//     smallImgs[0].classList.remove('sm-card')
//     smallImgs[1].classList.remove('sm-card')
//     smallImgs[2].classList.remove('sm-card')
//     smallImgs[3].classList.remove('sm-card')
//     smallImgs[4].classList.add('sm-card')
// })

// $(document).ready(function () {

//     // Function to get the CSRF token from the cookie
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 // Does this cookie string begin with the name we want?
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }

//     const csrftoken = getCookie('csrftoken');  // Get CSRF token

//     $("#add-to-cart-btn").on("click", function () {
//         let prod_quantity = $("#product-quantity").val();
//         let prod_title = $("#product-title").val();
//         let prod_id = $("#product-id").val();
//         let prod_price = $("#product-price").text();
//         let this_val = $(this);

//         $.ajax({
//             url: "/add-to-cart/",
//             type:'POST',
//             data: {
//                 'id': prod_id,
//                 'quant': prod_quantity,
//                 'title': prod_title,
//                 'title': prod_title,
//                 'price' : prod_price
//             },
//             headers: { 'X-CSRFToken': csrftoken },
//             beforeSend: function () {
//                 console.log({
//                     'id': prod_id,
//                     'quant': prod_quantity,
//                     'title': prod_title
//                 });
//                 console.log("Adding Product to Cart....");
//             },
//             success: function (response) {
//                 this_val.html("Item added to cart");
//                 console.log("Added product to Cart");
//                 console.log(response);  // Log the response to check the cart data
//                 $(".cart-items-count").text(response.totalcartitems);  // Update cart item count
//             },
//             error: function (xhr, status, error) {
//                 console.error("Error adding product to cart:", error);
//             }
//         });
//     });
// });

$(document).ready(function () {
    $("#add-to-cart-btn").on("click", function (event) {
        event.preventDefault();  // Prevent default behavior

        let prod_quantity = $("#product-quantity").val();
        let prod_id = $("#product-id").val();
        let prod_title = $("#product-title").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();  // Get CSRF token

        $.ajax({
            url: '/add-to-cart/',
            method: 'POST',
            data: {
                'id': prod_id,
                'quant': prod_quantity,
                'title': prod_title,
                'csrfmiddlewaretoken': csrf_token  // Include CSRF token in data
            },
            dataType: 'json',
            success: function (response) {
                alert('Item added to cart');
                $(".cart-items-count").text(response.totalcartitems);  // Update cart count
            },
            error: function (xhr, status, error) {
                console.error("Error adding item to cart:", error);
            }
        });
    });
});