import { EVENTS } from "./constants/events.mjs";
import { button, text } from "./constants/selectors.mjs";
import { dispatch } from "./utils.mjs";

let state = {};

function loadState() {
  dispatch({ type: EVENTS.LOAD_POPUP_STATE }).then(rootState => {
    console.log(rootState);
    state = rootState;
  });
}

loadState();

button.addEventListener("click", toggleStream);

function toggleStream() {
  state.started ? stop() : start();
}

function stop() {
  dispatch({ type: EVENTS.STOP_CAPTURE })
    .then(s => {
      state = s;
      return s;
    })
    .then(state => {
      text.innerHTML = state.started ? "stop energizer" : "start energizer";
    });
}

function start() {
  dispatch({ type: EVENTS.START_CAPTURE })
    .then(s => {
      state = s;
      return s;
    })
    .then(state => {
      text.innerHTML = state.started ? "stop energizer" : "start energizer";
    });
}
