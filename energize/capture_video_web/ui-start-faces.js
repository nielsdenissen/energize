(function() {
  const body = document.querySelector("body");

  function create(face) {
    const EMOJI_MAP = {
      "1": "😁",
      "0": "🙂",
      "-1": "😔"
    };
    const el = document.createElement("div");
    el.style.cssText = `
      background: rgba(255, 255, 255, 0.7);
      box-sizing: border-box;
      box-shadow:
        0 2px 2px 0 rgba(0,0,0,0.14),
        0 3px 1px -2px rgba(0,0,0,0.12),
        0 1px 5px 0 rgba(0,0,0,0.2);
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
    el.innerHTML = `
      <style>
        .emoji {
          font-size: 32px;
          margin-right: 12px;
        }
        .pointer {
          width: 0;
          height: 0;
          border-style: solid;
          border-width: 8px 10px 8px 0;
          border-color: transparent rgba(255, 255, 255, 0.7) transparent transparent;
          position: absolute;
          left: 0;
          top: 50%;
          transform: translate(-100%, -50%);
        }
      </style>
      <span class="pointer"></span>
      <span class="emoji">${EMOJI_MAP[face.expression.toString()] || "🤓"}</span>
      <span>${face.name}</span>
    `;
    return el;
  }

  function getId(face) {
    return `${ENERGIZER_CSS_PREFIX}__face__${snakeCase(face.name)}`;
  }

  function getElement(face) {
    return document.getElementById(getId(face));
  }

  function removeGone(faces) {
    const gone = current.filter(
      face => !faces.some(({ name }) => face.name === name)
    );
    gone.forEach(face => {
      const element = getElement(face);
      if (element) {
        body.removeChild(element);
      }
    });
    current = faces;
  }

  function position(el, face, imageSize) {
    const width = imageSize[1];
    const height = imageSize[0];
    const x = (face.location[1] / width) * window.innerWidth;
    const y = (face.location[0] / height) * window.innerHeight;
    el.style.transform = `translate(${x}px, ${y}px)`;
  }

  function snakeCase(string) {
    return string
      .replace(/\W+/g, " ")
      .split(/ |\B(?=[A-Z])/)
      .map(word => word.toLowerCase())
      .join("_");
  }

  function render(face, imageSize) {
    let el = getElement(face);
    if (el) {
      position(el, face, imageSize);
    } else {
      el = create(face);
      el.setAttribute("id", getId(face));
      position(el, face, imageSize);
      body.append(el);
      console.log("rendered face:", face.name);
    }
  }

  // store faces in variable in order to
  // determine which faces have gone and are to be removed
  let current = [];

  chrome.runtime.onMessage.addListener(function(request, sender, respond) {
    if (request.payload) {
      const { faces, image_size } = request.payload;
      console.log("received faces:", faces);
      removeGone(faces);
      faces.map(face => render(face, image_size));
    }
  });
})();
