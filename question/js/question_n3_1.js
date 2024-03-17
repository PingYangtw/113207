window.onload = function () {
    // Navbar
    renderNav();

    // 變數
    let tags = [];

    const defaultTags = ["白米", "糙米", "黑米", "紅米", "糯米", "香米", "小米",
        "寬麵", "細麵", "刀削麵", "拉麵", "義大利麵",
        "餃子", "餛飩", "麵包",
        "馬鈴薯", "玉米", "地瓜", "紅薯"];

    const tagListContainer1 = document.querySelector('.tag-list-item');
    const tagListContainer2 = document.querySelector('.tag-list-item2');
    const tagListContainer3 = document.querySelector('.tag-list-item3');
    const tagListContainer4 = document.querySelector('.tag-list-item4');

    const continueBtn = document.getElementById('continue-btn');

    const inputField = document.getElementById('tag-ip');

    const savedValue = sessionStorage.getItem('tagInputValue3');

    // 初始化標籤
    defaultTags.forEach((tag, index) => {
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

        if (index <= 7 ) {
            tagListContainer1.appendChild(tagButton);
        } else if (index <= 12) {
            tagListContainer2.appendChild(tagButton);
        } else if (index <= 15) {
            tagListContainer3.appendChild(tagButton);
        } else {
            tagListContainer4.appendChild(tagButton);
        }
    });

    function addTagToInput(tag) {
        tags.push(tag);

        // 將標籤文字添加到輸入框中
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
            continueBtn.classList.remove('button-gray');
            continueBtn.disabled = false;
        } else {
            continueBtn.classList.add('button-gray');
            continueBtn.classList.remove('button-brwon');
            continueBtn.disabled = true;
        }
    }

    // 点击按钮时跳转到question_second.html页面
    continueBtn.addEventListener('click', function () {
        const tagInput = document.getElementById('tag-ip');
        sessionStorage.setItem('tagInputValue3', tagInput.value);
        window.location.href = 'question_n4.html';
    });

    // 點擊返回按鈕時返回到前一頁
    document.getElementById('back').addEventListener('click', function () {
        const tagInput = document.getElementById('tag-ip');
        sessionStorage.setItem('tagInputValue3', tagInput.value);
        window.location.href = 'question_n3.html';
    });

   if (savedValue !== null) {
    inputField.value = savedValue;
    checkInput();
    const selectedTags = savedValue.split('、').map(tag => tag.trim());
    selectedTags.forEach(tag => {
        const tagButton = document.getElementById(tag);
        if (tagButton !== null) {
            tagButton.classList.add('item-select');
        }
    });
    
}
    
};


