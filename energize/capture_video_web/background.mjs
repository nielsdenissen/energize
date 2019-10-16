import { EVENTS } from "./constants/events.mjs";
import { logger } from "./config/logger.mjs";
import { getCurrentTab } from "./utils.mjs";
import { setup } from "./setup.mjs";

chrome.runtime.onInstalled.addListener(() => {
  logger.log("installed extension");
  setup();
});

const state = {
  started: false,
  tab: null,
  interval: null
};

chrome.runtime.onMessage.addListener((req, sender, res) => {
  switch (req.type) {
    case EVENTS.LOAD_POPUP_STATE: {
      return res(state);
    }
    case EVENTS.START_CAPTURE: {
      start();
      state.started = true;
      return res(state);
    }
    case EVENTS.STOP_CAPTURE: {
      stop();
      state.started = false;
      return res(state);
    }
  }
});

function socketSetup(tab) {
  const URL = "ws://localhost:5000/media";
  const socket = new WebSocket(URL);

  socket.onopen = () => {
    logger.log("sockets connection opened");
  };

  socket.onclose = () => {
    logger.log("socket connection closed");
  };

  socket.onerror = () => {
    socket.close();
    clearInterval(state.interval);
  }

  socket.onmessage = event => {
    logger.log(`received message from api: ${event}`);
    chrome.tabs.sendMessage(tab.id, {
      type: EVENTS.UPDATE_ENERGY,
      payload: JSON.parse(event.data)
    });
  };

  return socket;
}

let socket;

function start() {
  getCurrentTab().then(tab => {
    socket = socketSetup(tab);
    capture(tab);
    startUI(tab);
    state.tab = tab;
    logger.log('capture started');
  });
}

function stop() {
  stopUI(state.tab);
  socket.close();
}

function capture(tab) {
  const INTERVAL = 5000;
  state.interval = setInterval(function() {
    logger.log(`capture screenshot per ${INTERVAL}ms`);
    chrome.tabs.captureVisibleTab(tab.windowId, { format: "jpeg" }, blob => {
      socket.send(blob);
      logger.log(`captured screenshot sent`);
    });
  }, INTERVAL);
}

function startUI(tab) {
  logger.log('start ui script');
  chrome.tabs.executeScript(tab.id, {
    file: "./ui-start.js"
  });
}

function stopUI(tab) {
  logger.log('stop ui script');
  chrome.tabs.executeScript(tab.id, {
    file: "./ui-stop.js"
  });
}
