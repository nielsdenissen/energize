import { EVENTS } from "./constants/events.mjs";
import { socket } from "./config/sockets.mjs";
import { getCurrentTab } from "./utils.mjs";

chrome.runtime.onInstalled.addListener(() => {
  console.log("extension installed");

  chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
    chrome.declarativeContent.onPageChanged.addRules([
      {
        conditions: [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { hostContains: "meet.google.com" } // allow on meet.google.com
          }),
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { hostContains: "hangouts.google.com" } // allow on hangouts.google.com
          })
        ],
        actions: [new chrome.declarativeContent.ShowPageAction()]
      }
    ]);
  });

  const state = {
    started: false
  };

  chrome.runtime.onMessage.addListener((req, sender, res) => {
    switch (req.type) {
      case EVENTS.LOAD_POPUP_STATE: {
        return res(state);
      }
      case EVENTS.START_CAPTURE: {
        return start().then(() =>
          res({
            ...state,
            started: true
          })
        );
      }
      case EVENTS.STOP_CAPTURE: {
        return res({
          ...state,
          started: false
        });
      }
    }
  });
});

function start() {
  return getCurrentTab().then(tab => {
    capture(tab);
    initUI(tab);
  });
}

function capture(tab) {
  const INTERVAL = 5000;
  setInterval(function() {
    console.log(`capture every ${INTERVAL}ms`);
    chrome.tabs.captureVisibleTab(tab.windowId, { format: "jpeg" }, blob => {
      socket.send(blob);
      console.log(`screenshot sent`);
    });
  }, INTERVAL);
}

function initUI(tab) {
  chrome.tabs.executeScript(tab.id, {
    file: "./init-UI.js"
  });
}

socket.onmessage = event => {
  console.log(`received message from api: ${event}`);
  getCurrentTab().then(tab => {
    chrome.tabs.sendMessage(tab.id, {
      type: EVENTS.UPDATE_ENERGY,
      payload: JSON.parse(event.data)
    });
  });
};

/**
 * capture as video
 * 
function capture() {
  chrome.tabCapture.capture(
    {
      audio: true,
      video: true
    },
    stream => {
      video.srcObject = stream;
      video.style.display = "block";
      socket.send(stream);
    }
  );
}
*/
