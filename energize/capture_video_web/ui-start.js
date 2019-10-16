(function() {
  const body = document.querySelector("body");
  const ui = document.createElement("div");
  ui.setAttribute("id", "energizer__ui");

  ui.innerHTML = `
    <style>
      .container {
        position: fixed;
        bottom: 30px;
        left: 30px;
        width: 300px;
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
        font-size: 16px;
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
          <div>low</div>
          <div>medium</div>
          <div>high</div>
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
      const imageSize = request.payload.image_size;
      faces.map(face => renderFace(face, imageSize));
    }
  });

  function snakeCase(string) {
    return string
      .replace(/\W+/g, " ")
      .split(/ |\B(?=[A-Z])/)
      .map(word => word.toLowerCase())
      .join("_");
  }

  function updateMeter(energy) {
    const progress = document.getElementById("progress-bar");
    const percentage = Number(energy) > 5 ? Number(energy) : 5;
    progress.style.width = percentage + "%";
  }

  const EXPRESSION_EMOJI_TABLE = {
    Positive: "😁",
    Neutral: "🙂",
    Negative: "😔"
  };

  function renderFace(face, imageSize) {
    const elementId = `energizer__face__${snakeCase(face.name)}`;
    let element = document.getElementById(elementId);
    if (element) {
      getPosition(element);
    } else {
      element = document.createElement("div");
      element.style.cssText = `
        background: #fff;
        box-sizing: border-box;
        font-size: 18px;
        display: flex;
        position: fixed;
        top: 20px;
        align-items: center;
        left: 20px;
        border-radius: 4px;
        padding: 10px 18px;
        transition: transform 1000ms ease-in-out;
        z-index: 1;
      `;
      element.innerHTML = `
        <style>
          .emoji {
            font-size: 32px;
            margin-right: 12px;
          }
        </style>
        <span class="emoji">${EXPRESSION_EMOJI_TABLE[face.expression] ||
          "🤓"}</span>
        <span>${face.name}</span>
      `;
      element.setAttribute("id", elementId);
      getPosition(element);
      body.append(element);
      console.log(`rendered new element for ${face.name}`);
    }

    function getPosition(el) {
      const width = imageSize[1];
      const height = imageSize[0];
      const x = (face.location[1] / width) * window.innerWidth;
      const y = (face.location[0] / height) * window.innerHeight;
      el.style.transform = `translate(${x}px, ${y}px)`;
    }
  }
})();
