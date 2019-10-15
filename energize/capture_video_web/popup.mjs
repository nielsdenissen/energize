import { EVENTS } from "./constants/events.mjs";
import { button, text } from "./constants/selectors.mjs";
import { dispatch } from "./utils.mjs";

let state = {};

function loadState() {
  dispatch({ type: EVENTS.LOAD_POPUP_STATE }).then(update);
}

loadState();

button.addEventListener("click", toggleStream);

function toggleStream() {
  state.started ? stop() : start();
}

function stop() {
  dispatch({ type: EVENTS.STOP_CAPTURE }).then(update);
}

function start() {
  dispatch({ type: EVENTS.START_CAPTURE }).then(update);
}

function update(receivedState) {
  state = receivedState;
  text.innerHTML = receivedState.started ? "stop energizer" : "start energizer";
}
