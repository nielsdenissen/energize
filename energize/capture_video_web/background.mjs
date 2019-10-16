import { EVENTS } from "./constants/events.mjs";
import { WEB_SOCKET_URL } from "./constants/socket.mjs";
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
  let socket = new WebSocket(WEB_SOCKET_URL);

  socket.onopen = () => {
    logger.log("sockets connection opened");
  };

  socket.onclose = () => {
    logger.log("socket connection closed");
  };

  socket.onerror = error => {
    logger.log(`encountered error ${error}`);
    stop();

    logger.log("retrying socket connection");
    socket = new WebSocket(WEB_SOCKET_URL);
  };

  socket.onmessage = event => {
    const data = JSON.parse(event.data);
    logger.log("received message from api:", data);
    chrome.tabs.sendMessage(tab.id, {
      type: EVENTS.UPDATE_ENERGY,
      payload: data
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
    logger.log("capture started");
  });
}

function stop() {
  logger.log("stopping application");
  stopUI(state.tab);
  clearInterval(state.interval);
  socket.close(1000, "stopping application");
}

function capture(tab) {
  const INTERVAL = 2000;
  state.interval = setInterval(function() {
    logger.log(`capture screenshot per ${INTERVAL}ms`);
    chrome.tabs.captureVisibleTab(tab.windowId, { format: "jpeg" }, blob => {
      if (socket.readyState === socket.OPEN) {
        socket.send(blob);
      } else {
        logger.log("socket closed, retrying socket connection");
        socket = new WebSocket(WEB_SOCKET_URL);
      }
      logger.log(`captured screenshot sent`);
    });
  }, INTERVAL);
}

function startUI(tab) {
  logger.log("start ui script");
  chrome.tabs.executeScript(tab.id, {
    file: "./ui-start.js"
  });
}

function stopUI(tab) {
  logger.log("stop ui script");
  chrome.tabs.executeScript(tab.id, {
    file: "./ui-stop.js"
  });
}
