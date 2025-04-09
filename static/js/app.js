// Shared front-end behaviour lives here as pages need it.

function initStatusTabs() {
    const tabs = document.getElementById("status-tabs");
    const grid = document.getElementById("roster-grid");
    if (!tabs || !grid) return;

    tabs.addEventListener("click", (event) => {
        const tab = event.target.closest(".tab");
        if (!tab) return;

        tabs.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");

        const filter = tab.dataset.filter;
        grid.querySelectorAll(".card").forEach((card) => {
            const show = filter === "all" || card.dataset.status === filter;
            card.style.display = show ? "" : "none";
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initStatusTabs();
});
