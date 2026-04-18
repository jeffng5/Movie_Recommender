function setProgressPercent(p, labelText, root) {
  var scope = root && root.querySelector ? root : document;
  var bar = scope.querySelector("#bar");
  var onBar = scope.querySelector("#prog-pct-label");
  var raw = Number(p);
  var pClamped = Math.min(
    100,
    Math.max(0, Math.round(Number.isFinite(raw) ? raw : 0))
  );

  if (bar) {
    bar.style.width = pClamped + "%";
    bar.style.backgroundColor = "#00bfff";
  }
  if (onBar) {
    onBar.textContent =
      labelText !== undefined ? labelText : pClamped + "%";
  }
  return pClamped;
}

function startTask(button, id) {
  var root =
    button && button.closest ? button.closest("#rec-ele") : null;
  if (!root) root = document;

  var bar = root.querySelector("#bar");
  if (!bar) return;

  setProgressPercent(0, undefined, root);

  fetch("/recommendation/start/" + id, {
    method: "POST",
    headers: { Accept: "application/json" },
  })
    .then(function (res) {
      if (res.status === 409) {
        return res.json().then(function (j) {
          throw new Error(j.error || "Already in progress");
        });
      }
      if (!res.ok) throw new Error("Could not start recommendation");
      return res.json();
    })
    .then(function () {
      pollProgress(id, root);
    })
    .catch(function (err) {
      var msg = err.message || "Could not start";
      var short = msg.length > 24 ? msg.slice(0, 21) + "…" : msg;
      setProgressPercent(0, short, root);
    });
}

function pollProgress(id, root) {
  var interval = setInterval(function () {
    fetch("/progress?_=" + Date.now(), { cache: "no-store" })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        var scope = root && root.querySelector ? root : document;
        if (!scope.querySelector("#bar")) return;

        var pct = Number(data.percent);
        var p = setProgressPercent(
          Number.isFinite(pct) ? pct : 0,
          undefined,
          scope
        );

        if (data.error) {
          clearInterval(interval);
          var err = String(data.error);
          var short = err.length > 24 ? err.slice(0, 21) + "…" : err;
          setProgressPercent(0, short, scope);
          return;
        }

        var done =
          data.running === false &&
          (Number(data.percent) >= 100 || p >= 100);
        if (done) {
          clearInterval(interval);
          setProgressPercent(100, undefined, scope);
          setTimeout(function () {
            window.location.href = "/recommendation/" + id;
          }, 200);
        }
      })
      .catch(function () {
        clearInterval(interval);
      });
  }, 50);
}
