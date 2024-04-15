$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promo_promo_id").val(res.promo_id);
        $("#promo_cust_promo_code").val(res.cust_promo_code);
        $("#promo_type").val(res.type);
        $("#promo_value").val(res.value);
        $("#promo_quantity").val(res.quantity);
        $("#promo_start_date").val(res.start_date);
        $("#promo_end_date").val(res.end_date);
        if (res.active == true) {
            $("#promo_active").val("true");
        } else {
            $("#promo_active").val("false");
        }
        $("#promo_product_id").val(res.product_id);
        $("#promo_dev_created_at").val(res.dev_created_at);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promo_promo_id").val("");
        $("#promo_cust_promo_code").val("");
        $("#promo_type").val("");
        $("#promo_value").val("");
        $("#promo_quantity").val("");
        $("#promo_start_date").val("");
        $("#promo_end_date").val("");
        $("#promo_active").val("");
        $("#promo_product_id").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a promotion
    // ****************************************

    $("#create-btn").click(function () {

        let cust_promo_code = $("#promo_cust_promo_code").val();
        let type = $("#promo_type").val();
        let value = $("#promo_value").val();
        let quantity = $("#promo_quantity").val();
        let start_date = $("#promo_start_date").val();
        let end_date = $("#promo_end_date").val();
        let active = $("#promo_active").val() == "true";
        let product_id = $("#promo_product_id").val();
        let dev_created_at = new Date().toISOString().split('T')[0];

        let data = {
            "cust_promo_code": cust_promo_code,
            "type": type,
            "value": value,
            "quantity": quantity,
            "start_date": start_date,
            "end_date": end_date,
            "active": active,
            "product_id": product_id,
            "dev_created_at": dev_created_at
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a promotion
    // ****************************************

    $("#update-btn").click(function () {

        let promo_id = $("#promo_promo_id").val();
        let cust_promo_code = $("#promo_cust_promo_code").val();
        let type = $("#promo_type").val();
        let value = $("#promo_value").val();
        let quantity = $("#promo_quantity").val();
        let start_date = $("#promo_start_date").val();
        let end_date = $("#promo_end_date").val();
        let active = $("#promo_active").val() == "true";
        let product_id = $("#promo_product_id").val();
        let dev_created_at = new Date().toISOString().split('T')[0];

        let data = {
            "cust_promo_code": cust_promo_code,
            "type": type,
            "value": value,
            "quantity": quantity,
            "start_date": start_date,
            "end_date": end_date,
            "active": active,
            "product_id": product_id,
            "dev_created_at": dev_created_at
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/promotions/${promo_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Promotion has been Updated!")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        let promo_id = $("#promo_promo_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${promo_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let promo_id = $("#promo_promo_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${promo_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Promotion has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Cancel a promotion
    // ****************************************

    $("#cancel-btn").click(function () {

        let promo_id = $("#promo_promo_id").val();
        let cust_promo_code = $("#promo_cust_promo_code").val();
        let type = $("#promo_type").val();
        let value = $("#promo_value").val();
        let quantity = $("#promo_quantity").val();
        let start_date = $("#promo_start_date").val();
        let end_date = $("#promo_end_date").val();
        let active = $("#promo_active").val() == false;
        let product_id = $("#promo_product_id").val();

        let data = {
            "cust_promo_code": cust_promo_code,
            "type": type,
            "value": value,
            "quantity": quantity,
            "start_date": start_date,
            "end_date": end_date,
            "active": active,
            "product_id": product_id,
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/promotions/cancel/${promo_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Promotion has been Canceled!")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promo_promo_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a promotion
    // ****************************************

    $("#search-btn").click(function () {

        let cust_promo_code = $("#promo_cust_promo_code").val("");
        let type = $("#promo_type").val();
        let active = $("#promo_active").val() == "true";

        let queryString = ""

        if (cust_promo_code) {
            queryString += 'cust_promo_code=' + cust_promo_code
        }
        if (type) {
            if (queryString.length > 0) {
                queryString += '&type=' + type
            } else {
                queryString += 'type=' + type
            }
        }
        if (active) {
            if (queryString.length > 0) {
                queryString += '&active=' + active
            } else {
                queryString += 'active=' + active
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Promo ID</th>'
            table += '<th class="col-md-2">Cust Promo Code</th>'
            table += '<th class="col-md-2">Type</th>'
            table += '<th class="col-md-2">Value</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Start Date</th>'
            table += '<th class="col-md-2">End Date</th>'
            table += '<th class="col-md-2">Active</th>'
            table += '<th class="col-md-2">Product ID</th>'
            table += '<th class="col-md-2">Dev Created At</th>'
            table += '</tr></thead><tbody>'
            let firstPromotion = "";
            for (let i = 0; i < res.length; i++) {
                let promotions = res[i];
                table += `<tr id="row_${i}"><td>${promotions.promo_id}</td><td>${promotions.cust_promo_code}</td><td>${promotions.type}</td><td>${promotions.value}</td><td>${promotions.quantity}</td><td>${promotions.start_date}</td><td>${promotions.end_date}</td><td>${promotions.active}</td><td>${promotions.product_id}</td><td>${promotions.dev_created_at}</td></tr>`;
                if (i == 0) {
                    firstPromotion = promotions;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPromotion != "") {
                update_form_data(firstPromotion)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

})