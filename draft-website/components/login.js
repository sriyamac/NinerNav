//storing user info in local storage, need DB in future, and redirecting to main page
function storeUserInfoAndRedirect(event) {
    event.preventDefault(); // Prevent the form from submitting

    // const username = document.getElementById("username").value;
    const firstName = document.getElementById("firstName").value;
    // const lastName = document.getElementById("lastName").value;
    // const email = document.getElementById("email").value;

    const userInfo = /*`Username: ${username}, */ 'First Name: ${firstName}'; /*, Last Name: ${lastName}, Email: ${email}`; //putting it into userInfo */

    localStorage.setItem("userName", userInfo); //saving

    //sending user to main.html
    window.location.href = "signed-in.html";
}