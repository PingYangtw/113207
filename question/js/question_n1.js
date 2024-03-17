window.onload = function () {
    // Navbar
    renderNav();

    // 變數
    let tags = [];

    const defaultTags = ["低脂", "低碳水化合物", "低鈉",
        "高蛋白", "高纖維", "高能量", "減糖", "無糖",
        "孕婦或哺乳期飲食", "均衡營養"];

    const tagListContainer1 = document.querySelector('.tag-list-item');
    const tagListContainer2 = document.querySelector('.tag-list-item2');
    const tagListContainer3 = document.querySelector('.tag-list-item3');

    const continueBtn = document.getElementById('continue-btn');

    const inputField = document.getElementById('tag-ip');

    const savedValue = sessionStorage.getItem('tagInputValue');
    
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

        if (index >= 8) {
            tagListContainer3.appendChild(tagButton);
        } else if (index >= 3) {
            tagListContainer2.appendChild(tagButton);
        } else {
            tagListContainer1.appendChild(tagButton);
        }
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
        sessionStorage.setItem('tagInputValue', tagInput.value);
        window.location.href = 'question_n2.html';
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


