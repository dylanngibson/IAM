// nav.js - sidebar toggle script
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toggle").forEach(el => {
        el.addEventListener("click", () => {
            const tgt = document.getElementById(el.dataset.target);
            if (tgt) tgt.classList.toggle("hidden");
        });
    });
});