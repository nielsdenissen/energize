(function() {
  const body = document.querySelector("body");

  function init() {
    const monitor = document.createElement("div");
    monitor.setAttribute("id", `${ENERGIZER_CSS_PREFIX}__monitor`);
    monitor.innerHTML = `
      <style>
        .container {
          position: fixed;
          bottom: 30px;
          left: 30px;
          width: 300px;
          background: #fff;
          z-index: 1000;
          border-radius: 4px;
          box-shadow:
            0 2px 2px 0 rgba(0,0,0,0.14),
            0 3px 1px -2px rgba(0,0,0,0.12),
            0 1px 5px 0 rgba(0,0,0,0.2);
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
    body.append(monitor);
    console.log("energy monitor added");
  }

  function render(energy) {
    const MINIMUM = 5;
    const meter = document.getElementById("progress-bar");
    const percentage = energy <= MINIMUM ? MINIMUM : energy;
    meter.style.width = percentage + "%";
  }

  chrome.runtime.onMessage.addListener(function(request, sender, respond) {
    if (request.payload) {
      const energy = request.payload.energy;
      console.log("received energy:", energy);
      render(Number(energy));
    }
  });

  init();
})();
