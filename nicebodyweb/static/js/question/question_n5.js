window.onload = function() {
    // Navbar
    renderNav();

    if (messageText == "0") {
        document.getElementById("loginDialog").showModal();
        document.getElementById('loginDialog').scrollTop = 0;
    }

    // 變數
    let tags = [];

    const defaultTags = ["素食", "蛋", "牛奶", "無需求"];

    const tagListContainer1 = document.querySelector('.tag-list-item');

    const inputField = document.getElementById('tag-ip');

    const continueBtn = document.getElementById('continue-btn');

    const savedValue = sessionStorage.getItem('tagInputValue5');

    // Lottie
    var animation = bodymovin.loadAnimation({
        container: document.getElementById('animation-container'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: '/static/json/fruitJump.json' // 請替換為你的 JSON 動畫檔案路徑
    });

    // 初始化標籤
    defaultTags.forEach((tag) => {
        const tagButton = document.createElement("button");
        tagButton.classList.add("item");
        tagButton.textContent = tag;
        tagButton.id = tag;
        tagButton.addEventListener("click", function () {
            const isSelected = tagButton.classList.contains("item-select");
            if (!isSelected) {
                addTagToInput(tag); // 使用按鈕上存儲的標籤值
                tagButton.classList.add("item-select");
            } else {
                removeTagFromInput(tag); // 使用按鈕上存儲的標籤值
                tagButton.classList.remove("item-select");
            }
            
            // 每次点击标签后检查输入框
            checkInput();
        });
    
        tagListContainer1.appendChild(tagButton);

    });

    // 將標籤文字添加到輸入框中
    function addTagToInput(tag) {
        tags.push(tag);

        const tagInput = document.getElementById('tag-ip');
        if (tagInput.value.trim() === "") {
            tagInput.value = tag;
        } else {
            tagInput.value += `、 ${tag}`;
        }
    }

    // 從輸入框中移除指定的標籤文字
    function removeTagFromInput(tagToRemove) {
        
        tags = tags.filter(tag => tag !== tagToRemove);

        const tagInput = document.getElementById('tag-ip');
        const currentTags = tagInput.value.split('、').map(tag => tag.trim());
        const updatedTags = currentTags.filter(tag => tag !== tagToRemove);
        tagInput.value = updatedTags.join('、');
    }

    // 检查输入框中是否有文本，并根据情况更新按钮状态和样式
    function checkInput() {
        if (inputField.value.trim() !== '' || tags.length > 0) {
            continueBtn.classList.add('button-brwon');
            
            
        } else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    }

    inputField.addEventListener('input', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue !== '') {
            continueBtn.classList.add('button-brwon');
        } else {
            continueBtn.classList.remove('button-brwon');
        }
    });

    continueBtn.addEventListener('click', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue === '') {
            alert('請輸入內容');
        } else{
            const tagInputValue1 = sessionStorage.getItem('tagInputValue');
            const tagInputValue2 = sessionStorage.getItem('tagInputValue2');
            const tagInputValue3 = sessionStorage.getItem('tagInputValue3');
            const tagInputValue4_1 = sessionStorage.getItem('tagInputValue4_1');

            // 提交表單
            $.ajax({
                type: 'POST',
                url: '/question/resultRecipe',
                data: {
                    'tagInputValue1': tagInputValue1,
                    'tagInputValue2': tagInputValue2,
                    'tagInputValue3': tagInputValue3,
                    'tagInputValue4_1': tagInputValue4_1,
                    'tagInputValue5': inputValue
                },
                beforeSend: function() {
                    document.getElementById("loading").style.display = "flex";
                },
                success: function(data) {
                    const recipe_id = data.recipe_id;
                    window.location.href = `/robott/detailedRecipe?recipe_id=${recipe_id}`;
                },
                error: function() {
                    alert('發生錯誤，請稍後再試');
                }
            });

            sessionStorage.removeItem('tagInputValue');
            sessionStorage.removeItem('tagInputValue2');
            sessionStorage.removeItem('tagInputValue3');
            sessionStorage.removeItem('tagInputValue4_1');
            sessionStorage.removeItem('tagInputValue5');
        }
    });
};