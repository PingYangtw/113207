document.addEventListener("DOMContentLoaded", function() {
    const lockIcons = document.querySelectorAll('.lock-icon');
    const inputs = document.querySelectorAll('input');
    const saveButton = document.querySelector('.closesetting .button');
    const maleButton = document.getElementById('maleButton');
    const femaleButton = document.getElementById('femaleButton');
    let genderSelection = null; // 用於儲存選擇的性別

    // 初始化鎖定所有輸入框和按鈕
    lockAllInputs(true);
    setGenderButtonsDisabled(true);

    // 鎖圖標點擊事件
    lockIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            toggleAllLocks(false); // 解鎖全部
        });
    });

    // 性別按鈕點擊事件
    maleButton.addEventListener('click', function() {
        if (!maleButton.disabled) {
            selectGender('male');
        }
    });

    femaleButton.addEventListener('click', function() {
        if (!femaleButton.disabled) {
            selectGender('female');
        }
    });

    // 點擊 "變更個資" 按鈕後的行為
    saveButton.addEventListener('click', function() {
        toggleAllLocks(true); // 回復鎖定狀態
        lockAllInputs(true);
        setGenderButtonsDisabled(true);
        // 在這裡添加保存輸入數據的邏輯，例如通過AJAX發送到服務器
        console.log("資料已儲存");
    });

    function toggleInputLock(icon, lock) {
        const input = icon.closest('.title').nextElementSibling;
        if (lock) {
            icon.classList.remove('fa-unlock');
            icon.classList.add('fa-lock');
            if (input) {
                input.disabled = true; // 禁用輸入框
            }
        } else {
            icon.classList.remove('fa-lock');
            icon.classList.add('fa-unlock');
            if (input) {
                input.disabled = false; // 啟用輸入框
            }
        }
    }

    function toggleAllLocks(lock) {
        lockIcons.forEach(icon => {
            toggleInputLock(icon, lock);
        });
        inputs.forEach(input => input.disabled = lock);
        setGenderButtonsDisabled(lock);
    }

    function setGenderButtonsDisabled(disabled) {
        maleButton.disabled = disabled;
        femaleButton.disabled = disabled;
    }

    function selectGender(gender) {
        genderSelection = gender; // 儲存選擇的性別
        if (gender === 'male') {
            maleButton.style.border = "2px solid #297bcd";
            femaleButton.style.border = "none"; // 清除女性按鈕的邊框
        } else {
            femaleButton.style.border = "2px solid #c22574";
            maleButton.style.border = "none"; // 清除男性按鈕的邊框
        }
    }

    function lockAllInputs(lock) {
        inputs.forEach(input => {
            input.disabled = lock;
        });
        lockIcons.forEach(icon => {
            if (lock) {
                icon.classList.remove('fa-unlock');
                icon.classList.add('fa-lock');
            } else {
                icon.classList.remove('fa-lock');
                icon.classList.add('fa-unlock');
            }
        });
    }
});
