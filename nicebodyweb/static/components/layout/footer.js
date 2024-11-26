let renderFooter = function() {
  let footerStr = `
  <footer>
    <img src="/static/images/logo.jpg" alt="">
    <p>&copy;2024 nice巴底</p>
  </footer>
  `;

  document.getElementById("footer-container").innerHTML = footerStr;
}