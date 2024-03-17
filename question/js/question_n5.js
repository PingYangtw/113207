window.onload = function() {
    // Navbar
    renderNav();

    // 變數
    let tags = [];

    const defaultTags = ["素食", "無乳製品", "牛奶"];

    const tagListContainer1 = document.querySelector('.tag-list-item');

    const inputField = document.getElementById('tag-ip');

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
        const continueBtn = document.getElementById('continue-btn');
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

    // 點擊返回按鈕時返回到前一頁
    document.getElementById('back').addEventListener('click', function () {
        window.location.href = 'question_n4.html';
   });
};