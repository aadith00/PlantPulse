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
        let prod_quantity = $("#product-quantity").val();  // Make sure these IDs exist in your HTML
        let prod_title = $("#product-title").val();
        let prod_id = $("#product-id").val();
        let prod_price = $("#product-price").text();
        let this_val = $(this);

        console.log("Quantity:", prod_quantity);
        console.log("Title:", prod_title);
        console.log("ID:", prod_id);
        console.log("Price:", prod_price);
        console.log("Current Element:", this_val);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': prod_id,
                'quant': prod_quantity,
                'title': prod_title,  // Corrected here
                'price': prod_price
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding Product to Cart....");
            },
            success: function (response) {
                this_val.html("Item added to cart");
                console.log("Added product to Cart");
                $(".cart-items-count").text(response.totalcartitems)
            }
        });

    });
});


