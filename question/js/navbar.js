let renderNav = function() {
  let navStr = `
    <nav>
      <div class="area">
        <div class="logo">
          <img src="/images/logo.jpg" alt="">
          <h1>Nice巴底</h1>
        </div>
        <div class="middle">
          <div class="wrap">
            <a href="">Home</a>
            <a class="active" href="">Robot</a>
            <a href="">Goal</a>
            <a href="">Community</a>
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
      </div>
      <div class="sideBar" id="sideBar">
        <a href="">Home</a>
        <a class="active" href="">Robot</a>
        <a href="">Goal</a>
        <a href="">Community</a>
      </div>
    </nav>
  `;

  document.getElementById("nav-container").innerHTML = navStr;
}