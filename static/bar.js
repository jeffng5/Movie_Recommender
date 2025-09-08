
function startTask(id) {
    fetch(`/${id}`)
      .then(() => {
        pollProgress();
      });
  }

function pollProgress() {
    const interval = setInterval(() => {
      fetch("/progress")
        .then(res => res.json())
        .then(data => {
          document.getElementById("bar").style.width = data.percent + "%";
          document.getElementById("percent").textContent = data.percent + "%";
          if (data.percent >= 100) clearInterval(interval);
        });
    }, 500);
  }