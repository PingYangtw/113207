let renderNav = function() {
  let navStr = `
  <nav>
    <div class="area">
      <a href="/" class="logo">
        <img src="/static/images/logo2.png" alt="nicebodylogo">
        <h1>名food奇食</h1>
      </a>
      <div class="middle">
        <div class="wrap">
          <a href="/" class="nav-link">Home</a>
          <a href="/robott/generateRecipes" class="nav-link">Recipe</a>
          <a href="/goal/goalMain" class="nav-link">Record</a>
          <a href="/task/taskPage" class="nav-link">Task</a>
          <a href="/community/communityMain" class="nav-link">
            Q&A
            <div class="pro">
              <i class="fa-solid fa-crown"></i>
              pro
            </div>
          </a>
        </div>
        <div class="icon">
          <i class="fa-solid fa-bars" id="menuIcon"></i>
          <i class="fa-solid fa-xmark" id="closeIcon"></i>
        </div>
      </div>
      <div class="logSign" id="logSign" style="display: none;">
        <a href="/login/loginPage">Log in</a>
      </div>
      <div class="alreadyLogin" id="alreadyLogin" style="display: none;">
        <a href="/profile/profilePage" class="toprofile">
          <div class="nav-avatarFrame" style="display: none;">
            <img class="nav-profile" src="/static/images/userImage/${uid}/${userImage}" alt="ProfilePicture">
          </div>
          <img id="userImage" src="/static/images/userImage/${uid}/${userImage}" class="noAvatarFrame-nav-profile" alt="ProfilePicture">
          <h3 id="messageText">${messageText}</h3>
        </a>
        <a href="/login/logout">
          <i class="fa-solid fa-right-from-bracket"></i>
        </a>
      </div>
    </div>
  </nav>

  <div class="sideBar" id="sideBar">
    <div class="nav">
      <a href="/" class="nav-link">Home</a>
      <a href="/robott/generateRecipes" class="nav-link">Recipe</a>
      <a href="/goal/goalMain" class="nav-link">Record</a>
      <a href="/task/taskPage" class="nav-link">Task</a>
      <a href="/community/communityMain" class="nav-link">
        Q&A
        <div class="pro">
          <i class="fa-solid fa-crown"></i>
        </div>
      </a>
    </div>
  </div>
  `;

  document.getElementById("nav-container").innerHTML = navStr;

  if (messageText !== '0') {
    document.getElementById('alreadyLogin').style.display = 'flex';
  } else {
    document.getElementById('logSign').style.display = 'flex';
  }

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
