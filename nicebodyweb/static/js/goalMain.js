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

savecheck.addEventListener('click', function() {
    var textValue = document.getElementById('textcheck').value.trim();

    if (!lastClickedElement) {
    alert('請選擇一個圖示！');
    } else if (textValue === '') {
    alert('請輸入打卡目標！');
    } else {
    // 如果圖示和文字都有選擇，這裡可以放儲存資料的程式碼
    alert('打卡目標已儲存！');
    }
});

