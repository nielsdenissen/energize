export function setup() {
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
}
