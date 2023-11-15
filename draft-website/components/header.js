document.addEventListener("DOMContentLoaded", function() {
    const header = document.createElement("header");
    header.innerHTML = `
    <div class="banner">
        <h1>NinerNav</h1>
        <nav>
        <a href="main.html">Home Page</a> |
        <a href="login.html">Login</a> |
        <a href="gamepage.html">Game Page</a> |
        <a href="leaderboard.html">Leaderboard</a>
      </nav>
    </div>
      <br>
    `;
    document.body.insertBefore(header, document.body.firstChild);
  });  