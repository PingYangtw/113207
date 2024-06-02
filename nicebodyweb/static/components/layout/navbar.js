let renderNav = function() {
  let navStr = `
  <nav>
    <div class="area">
      <a href="/" class="logo">
        <img src="/static/images/logo.jpg" alt="nicebodylogo">
        <h1>Nice巴底</h1>
      </a>
      <div class="middle">
        <div class="wrap">
          <a href="/" class="nav-link">Home</a>
          <a href="/robott/generateRecipes" class="nav-link">Robot</a>
          <a href="/goal/goalMain" class="nav-link">Record</a>
          <a href="/task/taskPage" class="nav-link">Task</a>
          <a href="/community/communityMain" class="nav-link">Community</a>
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
        <a href="/profile/profilePage" class="toprofile">
          <img src="/static/images/user1.png" alt="">
          <h3>${messageText}</h3>
        </a>
        <a href="/login/loginPage">
          <i class="fa-solid fa-right-from-bracket"></i>
        </a>
      </div>
    </div>
  </nav>

  <div class="comunitynav" id="comunitynav">
    <div class="category">
      <h6>All</h6>
      <h6>Following</h6>
      <h6>My</h6>
    </div>
    <select>
      <option value="">all hashtag</option>
      <option value="">小知識</option>
    </select>
    <div class="search">
      <input type="search" placeholder="關鍵字查詢">
      <i class="fa-solid fa-magnifying-glass"></i>
    </div>
  </div>

  <div class="sideBar" id="sideBar">
    <div class="nav">
      <a href="/" class="nav-link">Home</a>
      <a href="/robott/generateRecipes" class="nav-link">Robot</a>
      <a href="/goal/goalMain" class="nav-link">Record</a>
      <a href="/task/taskPage" class="nav-link">Task</a>
      <a href="/community/communityMain" class="nav-link">Community</a>
    </div>
    <div class="sideBarcomunitynav">
      <h6>All</h6>
      <h6>Following</h6>
      <h6>My</h6>
      <select>
        <option value="">all hashtag</option>
        <option value="">小知識</option>
      </select>
      <div class="search">
        <input type="search" placeholder="關鍵字查詢">
        <i class="fa-solid fa-magnifying-glass"></i>
      </div>
    </div>
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

  const currentURL = window.location.pathname;
  const communitynav = document.getElementById('communitynav');

  if (currentURL === '/community/communityMain') {
    communitynav.style.display = 'flex';
  }
}