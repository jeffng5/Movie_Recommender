
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
          document.getElementById("bar").style.width = data.status + "%";
          document.getElementById("percent").textContent = data.status + "%";
          if (data.status >= 100) clearInterval(interval);
        });
    }, 500);
  }