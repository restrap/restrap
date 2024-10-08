/** @odoo-module **/

            //$('#add_to_cart').hide();

           const currentUrl = window.location.href;
           const product_id = $('.product_template_id').val();
           const product_id_variant = $('.product_id').val();

            console.log("11111111111111111111111",product_id,product_id_variant)


         $.ajax({
    url: "/collect-payment",
    type: "POST",
   data: JSON.stringify({ 
        value: "your_data_here",
        current_url: currentUrl,
        product_id: product_id,
        product_id_variant: product_id_variant // Include the current URL
    }),  // Convert data to JSON string if needed
    contentType: "application/json; charset=utf-8", // Set the content type to JSON
    dataType: "json", // Expect JSON response
    cache: false,

    success: function(res) {
        // Log the response for debugging
        console.log("Response:", res.result);

        // Check the result and show or hide the button accordingly
        if (res.result) { // Adjust this condition based on your actual response structure
            console.log("111111111111111111111111")
            $('#add_to_cart').show();
            $('.availability_messages').hide();
        } else {
             console.log("2222222222222222222222222")
            $('#add_to_cart').hide();
            $('.availability_messages').show();
        }

        // Optionally, you can also include a success message
    },

    error: function(xhr, status, error) {
        // Provide a more detailed error message if needed
        alert("An error occurred: " + xhr.responseText);
    }
});

$(document).ready(function() {
    const $inputs = $('input.js_variant_change');

    // Bind a change event to the variant inputs
    $inputs.on('change', function() {
        const currentUrl = window.location.href;
        const product_id = $('.product_template_id').val();
        const product_id_variant = $('.product_id').val();
        console.log("vvvvvvvvvvvvvvvvvvvvvvvv",product_id,product_id_variant)
        const product_id_variant_ids = $(this).val();

        // Log the input that triggered the event (optional)
        console.log("Variant changed:", $(this).val());

        $.ajax({
            url: "/collect-payment",
            type: "POST",
            data: JSON.stringify({
                value: "your_data_here",
                current_url: currentUrl,
                product_id: product_id,
                product_id_variant: product_id_variant,
                product_id_variant_ids:product_id_variant_ids
            }),  // Convert data to JSON string
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            cache: false,

            success: function(res) {
                console.log("Response:", res.result);

                // Show or hide the button based on the response
                if (res.result) {
                    console.log("Product is available.");
                    $('#add_to_cart').show();
                    $('.availability_messages').hide();
                } else {
                    console.log("Product is not available.");
                    $('#add_to_cart').hide();
                    $('.availability_messages').show();
                }
            },

            error: function(xhr, status, error) {
                alert("An error occurred: " + xhr.responseText);
            }
        });
    });
});


