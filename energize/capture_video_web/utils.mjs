export function dispatch(event) {
  console.log(`dispatched event ${event.type}`);
  return new Promise(resolve => {
    chrome.runtime.sendMessage(event, resolve);
  });
}

export function getCurrentTab(callback) {
  return new Promise(resolve => {
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
      resolve(tabs[0]);
    });
  });
}
