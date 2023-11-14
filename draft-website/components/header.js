document.addEventListener("DOMContentLoaded", function() {
    const header = document.createElement("header");
    header.innerHTML = `
    <div class="banner">
        <h1>NinerNav</h1>
        <button class="login-btn">Login</button>
    </div>
      <br>
    `;
    document.body.insertBefore(header, document.body.firstChild);
  });  