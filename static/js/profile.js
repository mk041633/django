const passwordField = document.querySelector("#PasswordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "Показать") {
      showPasswordToggle.textContent = "Скрыть";
      passwordField.setAttribute("type", "text");
    } else {
      showPasswordToggle.textContent = "Показать";
      passwordField.setAttribute("type", "password");
    }
  };
  
  showPasswordToggle.addEventListener("click", handleToggleInput);
  