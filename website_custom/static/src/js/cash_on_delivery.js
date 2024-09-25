/** @odoo-module **/

            //$('#add_to_cart').hide();
            
         $.ajax({
    url: "/collect-payment",
    type: "POST",
    data: JSON.stringify({ value: "your_data_here" }), // Convert data to JSON string if needed
    contentType: "application/json; charset=utf-8", // Set the content type to JSON
    dataType: "json", // Expect JSON response
    cache: false,

    success: function(res) {
        // Log the response for debugging
        console.log("Response:", res);

        // Check the result and show or hide the button accordingly
        if (res.result) { // Adjust this condition based on your actual response structure
            $('#add_to_cart').show();
        } else {
            $('#add_to_cart').hide();
        }

        // Optionally, you can also include a success message
    },

    error: function(xhr, status, error) {
        // Provide a more detailed error message if needed
        alert("An error occurred: " + xhr.responseText);
    }
});


