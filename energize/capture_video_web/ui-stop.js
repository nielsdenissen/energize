(function() {
  function cleanup() {
    const ui = document.getElementById('energizer__ui');
    if (ui) {
      document.querySelector('body').removeChild(ui);
    }
  }
  cleanup();
})();
