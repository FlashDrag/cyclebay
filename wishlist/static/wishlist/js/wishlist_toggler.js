$(document).ready(function () {
    // use the event delegation with .on() method by the reason that the class is added dynamically
    // $('.wishlist-toggler').click() works only for elements that are already present in the DOM
    // at the time the js loads
    $(document).on('click', '.wishlist-toggler', function () {
        const url = $(this).attr('data-url');
        const postData = { 'csrfmiddlewaretoken': csrfToken };
        const wishlistTogglerBtn = $(this);
        const productId = $(wishlistTogglerBtn).attr('data-product-id');

        $.post(url, postData).done(function (responce) {
            const msgContainer = $('.message-container');
            const ajaxMsgContainer = $('#ajax-message-container');
            const toastHeader = ajaxMsgContainer.find('.toast-header strong');
            const toastBody = ajaxMsgContainer.find('.toast-body');
            const toast = ajaxMsgContainer.find('.toast');

            // Attach message container to screen
            msgContainer.css({
                'position': 'fixed',
                'margin-top': '10px',
                'top': '25px',
                'right': '25px',
                'z-index': '1030'
            });
            toastHeader.text("Success!");
            toastBody.html(responce.wishlist_message);
            ajaxMsgContainer.removeClass('d-none');
            toast.toast('show');

            // If on wishlist page, remove card from DOM
            if ($(wishlistTogglerBtn).hasClass('on-wishlist')) {
                $('#card-product-'+ productId).remove();
            } else {
                // Otherwise, change button style based on is_in_wishlist value
                if (responce.is_in_wishlist) {
                    wishlistTogglerBtn.removeClass('btn-save');
                    wishlistTogglerBtn.addClass('btn-save-active');
                } else {
                    wishlistTogglerBtn.removeClass('btn-save-active');
                    wishlistTogglerBtn.addClass('btn-save');
                }
            }
        }).fail(function (xhr, textStatus, error) {
            alert(`Error:  ${xhr.status} ${error}! \nPlease, contact the administrator.`);
            console.error("Something went wrong in add_to_wishlist_toggle view");
        });
    });
});