(function() {
  const body = document.querySelector("body");
  const ui = document.createElement("div");
  ui.setAttribute('id', 'energizer__ui');

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

  body.append(ui);
  console.log("energy monitoring UI added");
  
  chrome.runtime.onMessage.addListener(function(request, sender, respond) {
    console.log("message received:", request);
    if (request.payload) {
      const energy = request.payload.energy;
      updateMeter(energy);

      const faces = request.payload.faces;
      faces.map(renderFace);
    }
  });

  function updateMeter(energy) {
    const progress = document.getElementById("progress-bar");
    progress.style.width = Number(energy) + "%";
  }

  const EXPRESSION_EMOJI_TABLE = {
    "Positive": "😁",
    "Neutral": "🙂",
    "Negative": "😔"
  }

  function renderFace(face) {
    const elementId = `energizer__face__${face.name}`;
    let element = document.getElementById(elementId);
    if (element) {
      // update element position
    } else {
      element = document.createElement("div");
      element.style.cssText = `
        background: #000000;
        color: white;
        box-sizing: border-box;
        font-size: 18px;
        display: flex;
        position: fixed;
        top: 20px;
        align-items: center;
        left: 20px;
        border-radius: 50px;
        padding: 8px 10px 10px 20px;
        z-index: 1;
      `
      element.innerHTML = `
        <style>
          .emoji {
            font-size:32px;
            margin-left: 12px;
          }
        </style>
        <span>${face.name}</span>
        <span>${EXPRESSION_EMOJI_TABLE[face.expression] || "🙃"}</span>
      `;
      element.setAttribute('id', `energizer__face__${face.name}`)
      body.append(element);
    }
  }
})();
