window.addEventListener("load", function () {
    (function ($) {
        function disable(checkbox) {
            checkbox.parent().parent('tr').find('.field-capacity > input[type="number"]').addClass('disabled');
        }

        function enable(checkbox) {
            checkbox.parent().parent('tr').find('.field-capacity > input[type="number"]').removeClass('disabled');
        }

        $('.field-has_capacity > input[type="checkbox"]').on('click', function () {
            const checkbox = $(this);
            if (checkbox.is(":checked")) {
                enable(checkbox);
            } else {
                disable(checkbox);
            }
        });

        $('.field-has_capacity > input[type="checkbox"]').each(function (index, elem) {
            const checkbox = $(elem);
            if (!checkbox.is(":checked")) {
                disable(checkbox);
            }
        })

    })(django.jQuery);
});