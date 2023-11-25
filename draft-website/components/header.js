document.addEventListener("DOMContentLoaded", function() {
    const header = document.createElement("header");
    header.innerHTML = `
    <div class="banner">
        <h1>NinerNav</h1>
        <nav>
        <a href="main.html">Home Page</a> |
        <a href="signed-in.html">Signed-In</a> |
        <a href="login.html">Login</a> |
        <a href="gameprep.html">Game Prep</a> |
        <a href="gamepage.html">Game Page</a> |
        <a href="leaderboard.html">Leaderboard</a> |
        <a href="resultpage.html">Result Page</a> |
        <a href="end-game.html">End Game Page</a>
      </nav>
    </div>
      <br>
    `;
    document.body.insertBefore(header, document.body.firstChild);
  });  