const passwordField1 = document.querySelector("#PasswordField1");
const passwordField2 = document.querySelector("#PasswordField2");
const showPasswordToggle1 = document.querySelector(".showPasswordToggle1");
const showPasswordToggle2 = document.querySelector(".showPasswordToggle2");

const handleToggleInput1 = (e) => {
  if (showPasswordToggle1.textContent === "Показать") {
    showPasswordToggle1.textContent = "Скрыть";
    passwordField1.setAttribute("type", "text");
  } else {
    showPasswordToggle1.textContent = "Показать";
    passwordField1.setAttribute("type", "password");
  }
};

showPasswordToggle1.addEventListener("click", handleToggleInput1);



const handleToggleInput2 = (e) => {
    if (showPasswordToggle2.textContent === "Показать") {
      showPasswordToggle2.textContent = "Скрыть";
      passwordField2.setAttribute("type", "text");
    } else {
      showPasswordToggle2.textContent = "Показать";
      passwordField2.setAttribute("type", "password");
    }
  };
  
  showPasswordToggle2.addEventListener("click", handleToggleInput2);

