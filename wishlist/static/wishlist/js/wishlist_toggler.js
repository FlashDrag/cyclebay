$(document).ready(function () {
    $('.wishlist-toggler').click(function () {
        const url = $(this).data('url');
        const postData = { 'csrfmiddlewaretoken': csrfToken };
        const wishlistTogglerBtn = $(this);

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

            // Change button style based on is_in_wishlist value
            if (responce.is_in_wishlist) {
                wishlistTogglerBtn.removeClass('btn-outline-dark');
                wishlistTogglerBtn.addClass('btn-dark');
            } else {
                wishlistTogglerBtn.removeClass('btn-dark');
                wishlistTogglerBtn.addClass('btn-outline-dark');
            }
        }).fail(function (xhr, textStatus, error) {
            // TODO: return error page based on status code 'xhr.status', e.g. 404, 500, etc.
            alert(`Error:  ${xhr.status} ${error}! \nPlease, contact the administrator.`);
            console.error("Something went wrong in add_to_wishlist_toggle view");
        })
    });
});