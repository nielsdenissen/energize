(function() {
  function cleanup() {
    const elements = document.querySelectorAll('[id^="energizer"]');
    if (elements.length) {
      for (let element of elements) {
        document.querySelector('body').removeChild(element);
      }
    }
  }
  cleanup();
})();
