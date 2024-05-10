$(document).ready(function() {
    $('input[type="checkbox"]').change(function() {
        var isChecked = $(this).prop("checked");
        var goalId = $(this).data("id");
        $.ajax({
            type: "POST",
            url: "/goal/goalMain",
            data: JSON.stringify({ checked: isChecked, id: goalId }),
            contentType: "application/json",
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});