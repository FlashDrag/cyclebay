// Collapse element functionality for the add new items(category,brand,color) forms
// in the store owner dashboard

$(document).ready(function () {
    const elementPrefixes = ['category', 'brand', 'color'];

    /**
     * Set up collapse handlers for each element
     * @param {string} elementPrefix - The prefix of the element (category, brand, color)
     * */
    function setUpCollapseHandlers(elementPrefix) {
        const capitalizedElementPrefix = elementPrefix.substring(0, 1).toUpperCase() + elementPrefix.substring(1);
        const collapseId = `#collapseNew${capitalizedElementPrefix}`;
        const newElementInputId = `#id_new_${elementPrefix}_name`;
        const defaultContainerDivId = `#div_id_${elementPrefix}`;
        const defaultSelect = `#div_id_${elementPrefix} select`;
        const toggleButton = `#new-${elementPrefix}-container button:first-child`;

        // New element collapse element
        $(collapseId).on('show.bs.collapse', function () {
            // set the new element name input to required
            $(newElementInputId).attr('required', true);
            // smoothly transition the margin of the div to 0
            $(defaultContainerDivId).animate({
                marginBottom: "0"
            }, 400);
            // smoothly hide the default element select, and set it to not required
            $(defaultSelect).hide('swing').attr('required', false);
            // change the toggle button to cancel
            $(toggleButton).removeClass('btn-outline-info').addClass('btn-outline-warning').html('<i class="fas fa-minus"></i> Cancel');
        });

        // set focus on the new element name input when the collapse is shown
        $(collapseId).on('shown.bs.collapse', function () {
            $(newElementInputId).focus();
        });

        // if new element is cancelled, revert to select element
        $(collapseId).on('hide.bs.collapse', function () {
            // set the new element name input to not required
            $(newElementInputId).attr('required', false);
            // smoothly revert the margin of the div to 1rem
            $(defaultContainerDivId).animate({
                marginBottom: "1rem"
            }, 400);
            // smoothly show the select element and set it to required
            $(defaultSelect).show('swing').attr('required', true);
            // revert the toggle button to its original state
            $(toggleButton).removeClass('btn-outline-warning').addClass('btn-outline-info').html(`<i class="fas fa-plus"></i> Add new ${capitalizedElementPrefix} to database`);
            $(newElementInputId).val('');
        });
    }

    // Set up collapse handlers for each element
    for (let prefix of elementPrefixes) {
        setUpCollapseHandlers(prefix);
    }


    /**
     * Expand the collapse element if there is a validation error in the new element input
     * @param {string} elementPrefix - The prefix of the element (category, brand, color)
     * */
    function collapseElementIfError(elementPrefix) {
        const collapseId = `#collapseNew${elementPrefix.substring(0, 1).toUpperCase() + elementPrefix.substring(1)}`;
        const newElementInputId = `#id_new_${elementPrefix}_name`;

        if ($(newElementInputId).hasClass('is-invalid')) {
            $(collapseId).collapse('show');
        }
    }

    for (let prefix of elementPrefixes) {
        collapseElementIfError(prefix);
    }


    // __Color picker__
    // https://bgrins.github.io/spectrum/
    $("#colorpicker").spectrum({
        preferredFormat: "hex",
        color: "#800080",
        clickoutFiresChange: true,
        showInput: true,
        showInitial: true,
        change: function (color) {
            $("#colorpicker").css("background-color", color.toHexString());
            $("#id_new_color_name").val(color.toHexString());
        }
    });
});