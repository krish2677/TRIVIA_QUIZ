let timer = 30;
const timerEl = document.getElementById('timer');

function updateTimer() {
    if (timer > 0) {
        timer--;
        timerEl.textContent = timer;
    } else {
        document.querySelector("form").submit(); // auto-submit when timer ends
    }
}
if (timerEl) {
    setInterval(updateTimer, 1000);
}
