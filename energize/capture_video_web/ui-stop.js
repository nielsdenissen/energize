(function() {
  function cleanup() {
    const elements = document.querySelectorAll(`[id^="${ENERGIZER_CSS_PREFIX}"]`);
    if (elements.length) {
      for (let element of elements) {
        document.querySelector('body').removeChild(element);
      }
    }
  }
  cleanup();
})();
