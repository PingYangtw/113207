let renderNav = function() {
  let navStr = `
    <nav>
      <div class="area">
        <div class="logo">
          <img src="/static/images/logo.jpg" alt="nicebodylogo">
          <h1>Nice巴底</h1>
        </div>
        <div class="middle">
          <div class="wrap">
            <a href="/" class="nav-link">Home</a>
            <a href="/robott/generateRecipes" class="nav-link">Robot</a>
            <a href="/goal/goalMain" class="nav-link">Record</a>
            <a href="/task/taskPage" class="nav-link">Task</a>
            <a href="/community/airecipePost" class="nav-link">Community</a>
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
          <a href="/profile/profilePage">
            <img src="/static/images/user1.png" alt="">
            <h3>${messageText}</h3>
          </a>
          <i class="fa-solid fa-right-from-bracket"></i>
        </div>
      </div>
    </nav>
    <div class="sideBar" id="sideBar">
      <a href="/" class="nav-link">Home</a>
      <a href="/robott/generateRecipes" class="nav-link">Robot</a>
      <a href="/goal/goalMain" class="nav-link">Record</a>
      <a href="/task/taskPage" class="nav-link">Task</a>
      <a href="/community/airecipePost" class="nav-link">Community</a>
    </div>
  `;

  document.getElementById("nav-container").innerHTML = navStr;

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

  const menuIcon = document.getElementById('menuIcon');
  const closeIcon = document.getElementById('closeIcon');
  const sideBar = document.getElementById('sideBar');

  menuIcon.addEventListener('click', function () {
    sideBar.style.display = 'flex';
    menuIcon.style.display = 'none';
    closeIcon.style.display = 'block';
  });

  closeIcon.addEventListener('click', function () {
    sideBar.style.display = 'none';
    closeIcon.style.display = 'none';
    menuIcon.style.display = 'block';
  });
}