let messageText = "{{data}}";
window.onload = function() {
    // Navbar
    renderNav();

    //變數
    const numberInputs = document.querySelectorAll('input[type="number"]');
    const checkbox1 = document.getElementById('checkbox1');
    const checkbox2 = document.getElementById('checkbox2');
    const min1 = document.getElementById('min_1');
    const max1 = document.getElementById('max_1');
    const continueBtn = document.getElementById('continue-btn');

    const savedValue1 = sessionStorage.getItem('tagInputValue4_1');
    const savedValue2 = sessionStorage.getItem('tagInputValue4_2')
    
    continueBtn.addEventListener('click', function () {
        if (checkbox1.checked) {
            sessionStorage.setItem('checkbox1Checked', 'true');
        } else if (checkbox2.checked) {
            sessionStorage.setItem('checkbox2Checked', 'true');
        }
        
        sessionStorage.setItem('tagInputValue4_1', min1.value);
        sessionStorage.setItem('tagInputValue4_2', max1.value);
        sessionStorage.removeItem('tagInputValue5');
    });

    // 监听checkbox1的变化事件
    checkbox1.addEventListener('change', function() {
        if (this.checked) {
            checkbox2.checked = false; // 如果checkbox1被勾选，则取消checkbox2的勾选
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n5');
        }else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    });

    // 监听checkbox2的变化事件
    checkbox2.addEventListener('change', function() {
        if (this.checked) {
            checkbox1.checked = false; // 如果checkbox2被勾选，则取消checkbox1的勾选
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n5');
        }else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    });

    numberInputs.forEach(function(input) {
        // 当输入框失去焦点时检查输入值是否为负数
        input.addEventListener('blur', function() {
            if (parseInt(this.value) < 0) {
                // 如果输入值为负数，将其设为0
                this.value = 0;
            }
        });
    });

    if (savedValue1 !== null) {
        checkbox1.value = savedValue1;
        continueBtn.classList.add('button-brwon');
        continueBtn.setAttribute('href', '/question/question_n5');
        
    }

    if (savedValue1 !== null || savedValue2 !== null) {
        min1.value = savedValue1;
        max1.value = savedValue2;
        continueBtn.classList.add('button-brwon');
        continueBtn.setAttribute('href', '/question/question_n5');
        
    }

    if (savedValue1 !== null) {
        min1.value = savedValue1;
    }

    if (savedValue2 !== null) {
        max1.value = savedValue2;
    }

};