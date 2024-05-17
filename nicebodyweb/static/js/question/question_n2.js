let messageText = "{{data}}";
window.onload = function() {
    // Navbar
    renderNav();

    // 變數
    const buttons = document.querySelectorAll('.type');

    const darkGreenColor = '#92ae9e';

    const continueBtn = document.getElementById('continue-btn');

    const inputField = document.getElementById('tag-ip');

    const savedValue = sessionStorage.getItem('tagInputValue2');

    const savedSelectedTag1Count = sessionStorage.getItem('selectedTag1Count');

    // 鼠標經過按鈕時改變背景顏色
    buttons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.transition = 'background-color 0.5s ease'; // 添加過渡效果
            button.style.backgroundColor = darkGreenColor;
        });
    
        button.addEventListener('mouseout', () => {
            button.style.transition = 'background-color 0.5s ease'; // 添加過渡效果
            button.style.backgroundColor = '';
        });
    });

    // 检查输入框中是否有文本，并根据情况更新按钮状态和样式
    function checkInput() {
        const continueBtn = document.getElementById('continue-btn');
        if (inputField.value.trim() !== '' || tags.length > 0) {
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n3');
        } else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    }

    inputField.addEventListener('input', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue !== '') {
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n3');
        } else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    });

    continueBtn.addEventListener('click', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue === '') {
            alert('請輸入內容');
        } 
    });

    if (savedSelectedTag1Count !== null) {
        const selectedTag1Count = parseInt(savedSelectedTag1Count);
        const tag1Button = document.getElementById('n2_1');
        const tag1Div = tag1Button.querySelector('div');
        if (selectedTag1Count > 0) {
            tag1Div.textContent += `+${selectedTag1Count}`;
            tag1Button.classList.add('select');
        }
    }

    // 点击按钮时跳转到question_second.html页面
    continueBtn.addEventListener('click', function () {
        const tagInput = document.getElementById('tag-ip');
        sessionStorage.setItem('tagInputValue2', tagInput.value);
        sessionStorage.removeItem('tagInputValue3');
    });

    
    document.getElementById('n2_1').addEventListener('click', function() {
        const tagInput = document.getElementById('tag-ip');
        sessionStorage.setItem('tagInputValue2', tagInput.value);
    });

    if (savedValue !== null) {
        inputField.value = savedValue;
        checkInput();
        
    }
};