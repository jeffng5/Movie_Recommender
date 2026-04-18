function setProgressPercent(p, labelText) {
  const bar = document.getElementById("bar");
  const onBar = document.getElementById("prog-pct-label");
  const raw = Number(p);
  const pClamped = Math.min(
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

function startTask(id) {
  const bar = document.getElementById("bar");
  if (!bar) return;

  setProgressPercent(0);

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
      pollProgress(id);
    })
    .catch(function (err) {
      const msg = err.message || "Could not start";
      const short = msg.length > 24 ? msg.slice(0, 21) + "…" : msg;
      setProgressPercent(0, short);
    });
}

function pollProgress(id) {
  const interval = setInterval(function () {
    fetch("/progress")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (!document.getElementById("bar")) return;

        const p = setProgressPercent(data.percent);

        if (data.error) {
          clearInterval(interval);
          const err = String(data.error);
          const short = err.length > 24 ? err.slice(0, 21) + "…" : err;
          setProgressPercent(0, short);
          return;
        }

        if (data.running === false && p >= 100) {
          clearInterval(interval);
          setProgressPercent(100);
          setTimeout(function () {
            window.location.href = "/recommendation/" + id;
          }, 200);
        }
      })
      .catch(function () {
        clearInterval(interval);
      });
  }, 400);
}
