const showPasswordToggle = document.querySelector(".showPasswordToggle")
const PasswordField = document.querySelector("#PasswordField")


const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "Показать"){
        showPasswordToggle.textContent = "Скрыть";
        PasswordField.setAttribute("type", "text");
    }
    else {
        showPasswordToggle.textContent = "Показать";
        PasswordField.setAttribute("type", "password");

    }

};
showPasswordToggle.addEventListener("click", handleToggleInput);
