'use strict';

window.onload = function () {
    console.log('DOM ready');
    // let basket = document.querySelector('.basket_list');
    // basket.onchange = function (e) {
    //     console.log('target', e.target);
    // }
    let basketList = $('.basket_list');
    basketList.on('change', 'input[type=number].product_qty', function (event) {
        // console.log(event.target);
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                // console.log(data);
                basketList.html(data.basket_items);
                // $('.basket_summary')...
            },
        });
    })
}