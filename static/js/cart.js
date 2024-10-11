let featuedImg = document.getElementById('featured-image');
let smallImgs = document.getElementsByClassName('small-Img');

smallImgs[0].addEventListener('click', () => {
    featuedImg.src = smallImgs[0].src;
    smallImgs[0].classList.add('sm-card')
    smallImgs[1].classList.remove('sm-card')
    smallImgs[2].classList.remove('sm-card')
    smallImgs[3].classList.remove('sm-card')
    smallImgs[4].classList.remove('sm-card')
})
smallImgs[1].addEventListener('click', () => {
    featuedImg.src = smallImgs[1].src;
    smallImgs[0].classList.remove('sm-card')
    smallImgs[1].classList.add('sm-card')
    smallImgs[2].classList.remove('sm-card')
    smallImgs[3].classList.remove('sm-card')
    smallImgs[4].classList.remove('sm-card')
})
smallImgs[2].addEventListener('click', () => {
    featuedImg.src = smallImgs[2].src;
    smallImgs[0].classList.remove('sm-card')
    smallImgs[1].classList.remove('sm-card')
    smallImgs[2].classList.add('sm-card')
    smallImgs[3].classList.remove('sm-card')
    smallImgs[4].classList.remove('sm-card')
})
smallImgs[3].addEventListener('click', () => {
    featuedImg.src = smallImgs[3].src;
    smallImgs[0].classList.remove('sm-card')
    smallImgs[1].classList.remove('sm-card')
    smallImgs[2].classList.remove('sm-card')
    smallImgs[3].classList.add('sm-card')
    smallImgs[4].classList.remove('sm-card')
})
smallImgs[4].addEventListener('click', () => {
    featuedImg.src = smallImgs[4].src;
    smallImgs[0].classList.remove('sm-card')
    smallImgs[1].classList.remove('sm-card')
    smallImgs[2].classList.remove('sm-card')
    smallImgs[3].classList.remove('sm-card')
    smallImgs[4].classList.add('sm-card')
})

$(document).ready(function () {
    $("#add-to-cart-btn").on("click", function () {
        let prod_quantity = $("#product-quantity").val();
        let prod_title = $("#product-title").val();
        let prod_id = $("#product-id").val();
        let this_val = $(this);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': prod_id,
                'quant': prod_quantity,
                'title': prod_title
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding Product to Cart....");
            },
            success: function (response) {
                this_val.html("Item added to cart");
                console.log("Added product to Cart");
                console.log(response);  // Log the response to check the cart data
                $(".cart-items-count").text(response.totalcartitems);  // Update cart item count
            },
            error: function (xhr, status, error) {
                console.error("Error adding product to cart:", error);
            }
        });
    });
});