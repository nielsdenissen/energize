const ui = document.createElement("div");

ui.innerHTML = `
    <style>
      .container {
        position: fixed;
        bottom: 30px;
        left: 30px;
        width: 300px;
        height: 100px;
        background: #fff;
        z-index: 1000;
        border-radius: 4px;
        box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2);
        padding: 20px;
        font-size: 22px;
      }
      .progress {
        margin-top: 20px;
        display: flex;
        flex-direction: column;
      }
      .progress-bar {
        background: linear-gradient(to right, red, yellow, green);
        height: 5px;
        position: relative;
        width: 100%;
        border-radius: 20px;
        transition: width 700ms ease;
      }
      .progress-legend {
        font-size: 32px;
        display: flex;
        margin-top: 12px;
        justify-content: space-between;
      }
    </style>
    <div class="container">
      <div>Overall energy level</div>
      <div class="progress">
        <div class="progress-bar" id="progress-bar"></div>
        <div class="progress-legend">
          <div>😔</div>
          <div>🙂</div>
          <div>😁</div>
        </div>
      </div>
    </div>
  `;

document.querySelector("body").append(ui);

console.log("initializing UI");

chrome.runtime.onMessage.addListener(function(req, sender, respond) {
  console.log("received message");
  const progress = document.getElementById("progress-bar");
  const width = Number(req.payload.energy) + "%";
  progress.style.width = width;
});
