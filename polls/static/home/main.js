let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let logo = document.querySelector(".logo_name");

// console.log(logo);

closeBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  // call function
  changeBtn();
});

function changeBtn() {
  if(sidebar.classList.contains("open")) {
    closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
    logo.style.display = 'none';
    //logo.style.display = (sidebar.style.width < 600 ) ? 'block' : 'none';
  } else {
    closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
    //logo.style.display = (sidebar.style.width < 600 ) ? 'block' : 'none';
    logo.style.display = 'block';
  }
}