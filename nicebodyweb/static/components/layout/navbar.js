let renderNav = function() {
  let navStr = `
    <nav>
      <div class="area">
        <div class="logo">
          <img src="/static/images/logo.jpg" alt="">
          <h1>Nice巴底</h1>
        </div>
        <div class="middle">
          <div class="wrap">
            <a href="/" class="nav-link">Home</a>
            <a href="/robott/generateRecipes" class="nav-link">Robot</a>
            <a href="" class="nav-link">Goal</a>
            <a href="" class="nav-link">Community</a>
          </div>
          <div class="icon">
            <i class="fa-solid fa-bars" id="menuIcon"></i>
            <i class="fa-solid fa-xmark" id="closeIcon"></i>
          </div>
        </div>
        <div class="logSign">
          <a href="">Log in</a>
          <a href="">Sign up</a>
        </div>
        <div class="alreadyLogin">
          <img src="/static/images/user1.png" alt="">
          <h3>${messageText}</h3>
          <i class="fa-solid fa-right-from-bracket"></i>
        </div>
      </div>
      <div class="sideBar" id="sideBar">
        <a href="">Home</a>
        <a href="">Robot</a>
        <a href="">Goal</a>
        <a href="">Community</a>
      </div>
    </nav>
  `;

  document.getElementById("nav-container").innerHTML = navStr;
        
  // 将新文本节点添加到 id 为 "test" 的元素中
  testElement.appendChild(newText);


  let navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {

      navLinks.forEach(link => {
        link.style.color = '#6E3D0D';
      });

      link.style.color = '#FFCF56';

      localStorage.setItem('activeLinkId', link.getAttribute('href'));
    });
  });

  let activeLinkId = localStorage.getItem('activeLinkId');
  if (activeLinkId) {
    let activeLink = document.querySelector(`[href="${activeLinkId}"]`);
    if (activeLink) {
      activeLink.style.color = '#FFCF56';
    }
  }
}