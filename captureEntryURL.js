javascript: (function () {
  if (window.itfTennisObserver) {
    alert("Already running!");
    return;
  }

  let observer = new PerformanceObserver((list) => {
    let entries = list.getEntries();
    for (let entry of entries) {
      if (
        entry.name.startsWith(
          "https://ipin.itftennis.com/Umbraco/Surface/entrylist/entry-list?tennisEventId"
        )
      ) {
        prompt("Captured Entry List URL:", entry.name);
      }
    }
  });

  observer.observe({ type: "resource", buffered: true });
  window.itfTennisObserver = observer;

  alert(
    "Request capture activated! URLs will appear in a popup when detected."
  );
})();
