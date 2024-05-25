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
        savecheck.disabled = true;

        // 創建新的元素
        var checkBox = document.createElement('div');
        checkBox.classList.add('item');

        var checkBoxInput = document.createElement('input');
        checkBoxInput.setAttribute('type', 'checkbox');

        var checkBoxLabel = document.createElement('label');
        checkBoxLabel.setAttribute('for', 'horns');

        var iconElement = document.createElement('i');
        var iconClass = lastClickedElement.querySelector('i').classList[1];
        iconElement.classList.add('fa-solid', iconClass);

        var textNode = document.createTextNode(textValue);

        // 將圖示和文字添加到標籤中
        checkBoxLabel.appendChild(document.createTextNode('\u2002')); // 添加空格
        checkBoxLabel.appendChild(iconElement);
        checkBoxLabel.appendChild(document.createTextNode('\u2002')); // 添加空格
        checkBoxLabel.appendChild(textNode);

        // 將元素添加到檢查框中
        checkBox.appendChild(checkBoxInput);
        checkBox.appendChild(checkBoxLabel);

        // 將檢查框添加到指定位置之前
        var checkContainer = document.querySelector('.check-box');
        var addCheckBox = document.querySelector('.add-check-box');
        checkContainer.insertBefore(checkBox, addCheckBox);
        
        switch (iconClass) {
            case 'fa-droplet':
                iconId = 1;
                break;
            case 'fa-seedling':
                iconId = 2;
                break;
            case 'fa-apple-whole':
                iconId = 3;
                break;
            case 'fa-cookie-bite':
                iconId = 4;
                break;
            case 'fa-martini-glass':
                iconId = 5;
                break;
            default:
                iconId = 0; // 如果沒有匹配的，設置為 0 或其他適當的默認值
        }

        // 發送 AJAX 請求將數據寫入資料庫
        $.ajax({
            type: "POST",
            url: "/goal/saveCheckbox",
            data: JSON.stringify({ iconId: iconId, text: textValue }),
            contentType: "application/json",
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });

        check.close();

        var icons = document.querySelectorAll('.iconbtn');
        icons.forEach(function(icon) {
        icon.removeAttribute('style'); // Remove inline style from the div
        var iconElement = icon.querySelector('i');
        if (iconElement) {
            iconElement.removeAttribute('style'); // Remove inline style from the i element
        }
        });
        document.getElementById('textcheck').value = '';

        savecheck.disabled = false;
    }
});

