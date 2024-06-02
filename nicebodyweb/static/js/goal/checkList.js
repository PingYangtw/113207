// const e = require("cors");

let currentRow = null;
let selectedIconType = null;

document.querySelectorAll('.opencheck').forEach(button => {
  button.addEventListener('click', function() {
    const goal = this.getAttribute('data-goal');
    const iconType = this.getAttribute('data-icon');
    const id = this.getAttribute('data-id');

    document.getElementById('goalInput').value = goal;
    highlightIcon(iconType);
    selectedIconType = iconType;

    currentRow = document.querySelector(`tr[data-id="${id}"]`);

    document.getElementById('check').showModal();
  });
});

document.querySelectorAll('.opencheck').forEach(button => {
    button.addEventListener('click', function() {
      const goal = this.getAttribute('data-goal');
      const iconType = this.getAttribute('data-icon');
      const id = this.getAttribute('data-id');
  
      document.getElementById('goalInput').value = goal;
      highlightIcon(iconType);
      selectedIconType = iconType;
  
      currentRow = document.querySelector(`tr[data-id="${id}"]`);
  
      document.getElementById('check').showModal();
    });
  });

document.getElementById('closecheck').addEventListener('click', function() {
  document.getElementById('check').close();
});

var lastClickedElement = null;

function changeColor(element) {
  var iconName = element.classList[1].replace("iconbtn-", "");
  element.style.backgroundColor = getColor(iconName);
  element.querySelector("i").style.color = "#ffffff";

  // Reset color of last clicked element
  if (lastClickedElement && lastClickedElement !== element) {
    resetColor(lastClickedElement);
  }

  lastClickedElement = element;
  selectedIconType = element.getAttribute('data-icon');
}

function resetColor(element) {
  element.style.backgroundColor = '';
  element.querySelector("i").style.color = '';
}

function getColor(iconName) {
  switch(iconName) {
    case "droplet":
      return "#59A5D8";
    case "seedling":
      return "#4AD66D";
    case "martini-glass":
      return "#FF9914";
    case "cookie-bite":
      return "#BC6C25";
    case "apple-whole":
      return "#e5446d";
    default:
      return "#ffffff";
  }
}

function highlightIcon(iconType) {
  const iconClass = `iconbtn-${getIconClass(iconType)}`;
  document.querySelectorAll('.iconbtn').forEach(icon => {
    if (icon.classList.contains(iconClass)) {
      changeColor(icon);
    } else {
      resetColor(icon);
    }
  });
}

function getIconClass(iconType) {
  switch(iconType) {
    case '1':
      return "droplet";
    case '2':
      return "seedling";
    case '3':
      return "martini-glass";
    case '4':
      return "cookie-bite";
    case '5':
      return "apple-whole";
    default:
      return "";
  }
}

document.getElementById('savecheck').addEventListener('click', function() {
  var textValue = document.getElementById('goalInput').value.trim();

  if (textValue === '') {
    alert('請輸入打卡目標！');
  } else if (currentRow) {
    currentRow.querySelector('.goal-cell').textContent = textValue;

    const iconCell = currentRow.querySelector('.icon-cell');
    iconCell.innerHTML = '';

    let iconHtml = '';
    switch(selectedIconType) {
        case '1':
          iconHtml = '<i class="fa-solid fa-droplet" data-icon="droplet"></i>';
          break;
        case '2':
          iconHtml = '<i class="fa-solid fa-seedling" data-icon="seedling"></i>';
          break;
        case '3':
          iconHtml = '<i class="fa-solid fa-martini-glass" data-icon="martini-glass"></i>';
          break;
        case '4':
          iconHtml = '<i class="fa-solid fa-cookie-bite" data-icon="cookie-bite"></i>';
          break;
        case '5':
          iconHtml = '<i class="fa-solid fa-apple-whole" data-icon="apple-whole"></i>';
          break;
    }
    
    // 發送 AJAX 請求將數據寫入資料庫
    $.ajax({
    type: "POST",
    url: "/goal/updateCheckbox",
    data: JSON.stringify({ iconId: selectedIconType, text: textValue, id : currentRow.getAttribute('data-id')}),
    contentType: "application/json",
        success: function(response) {
            console.log(response);
        },
        error: function(xhr, status, error) {
            console.error(error);
            alert(error, '出現錯誤，請稍後再試！');
        }
    });

    iconCell.innerHTML = iconHtml;

    // 更新 opencheck 按鈕的 data-goal 和 data-icon 屬性
    const editButton = currentRow.querySelector('.opencheck');
    editButton.setAttribute('data-goal', textValue);
    editButton.setAttribute('data-icon', selectedIconType);

    document.getElementById('check').close();
    
  }
});

//delete goal
document.querySelectorAll('.opencheck').forEach(button => {
    button.addEventListener('click', function() {
      const goal = this.getAttribute('data-goal');
      const iconType = this.getAttribute('data-icon');
      const id = this.getAttribute('data-id');
  
      document.getElementById('goalInput').value = goal;
      highlightIcon(iconType);
      selectedIconType = iconType;
  
      currentRow = document.querySelector(`tr[data-id="${id}"]`);
  
      document.getElementById('check').showModal();
    });
  });

document.querySelectorAll('.opendelete').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.getAttribute('data-id');
        currentRow = document.querySelector(`tr[data-id="${id}"]`);
    
        document.getElementById('delete').showModal();
    });
});

document.getElementById('savedelete').addEventListener('click', function() {
    if (currentRow) {
        const id = currentRow.getAttribute('data-id');
        $.ajax({
            type: "POST",
            url: "/goal/deleteCheckbox",
            data: JSON.stringify({ id: id }),
            contentType: "application/json",
            success: function(response) {
                console.log(response);
                
            },
            error: function(xhr, status, error) {
                console.error(error);
                alert(error, '出現錯誤，請稍後再試！');
            }
        });
        currentRow.remove();
        document.getElementById('delete').close();
    }
});

document.getElementById('closedelete').addEventListener('click', function() {
    document.getElementById('delete').close();
});

// 關鍵字查詢
document.getElementById('searchInput').addEventListener('input', function() {
  var searchText = this.value.toLowerCase();
  var rows = document.querySelectorAll('table tr[data-id]');

  rows.forEach(function(row) {
      var goalText = row.querySelector('.goal-cell').textContent.toLowerCase();
      if (goalText.includes(searchText)) {
          row.style.display = '';
      } else {
          row.style.display = 'none';
      }
  });
});