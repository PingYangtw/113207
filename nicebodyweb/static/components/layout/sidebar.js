document.addEventListener('DOMContentLoaded', function () {
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
});