function renderPanel(student) {
    const panel = document.getElementById("detail-panel");
    const initial = student.name ? student.name[0].toUpperCase() : "?";

    panel.innerHTML = `
        <div class="thumb-lg">${initial}</div>
        <h2>${student.name}</h2>
        <p class="meta">${student.student_id} · ${student.program || "No program set"}</p>

        <button class="btn btn-primary">Mark Present</button>
        <button class="btn btn-secondary">▶ View History</button>

        <div class="stat-row"><span class="label">Enrolled</span><span>${student.enrolled}</span></div>
        <div class="stat-row"><span class="label">Last seen</span><span>${student.last_seen || "never"}</span></div>
        <div class="stat-row"><span class="label">Attendance rate</span><span>${student.attendance_rate}%</span></div>
    `;
}

function initRosterClicks() {
    const grid = document.getElementById("roster-grid") || document.getElementById("student-grid");
    if (!grid) return;

    grid.addEventListener("click", async (event) => {
        const card = event.target.closest(".card[data-id]");
        if (!card) return;

        const res = await fetch(`/api/students/${card.dataset.id}`);
        if (!res.ok) return;
        renderPanel(await res.json());
    });
}

document.addEventListener("DOMContentLoaded", initRosterClicks);
