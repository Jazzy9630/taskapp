// TaskFlow frontend logic — Jahanzaib Muhammad
const API_BASE = "/api/todos";

const listEl = document.getElementById("taskList");
const formEl = document.getElementById("newTaskForm");
const inputEl = document.getElementById("titleField");
const emptyStateEl = document.getElementById("emptyState");
const tabButtons = document.querySelectorAll(".tab");

let cachedTasks = [];
let currentFilter = "all";

async function loadTasks() {
    const res = await fetch(API_BASE);
    cachedTasks = await res.json();
    render();
}

function render() {
    const visible = cachedTasks.filter((t) => {
        if (currentFilter === "active") return !t.done;
        if (currentFilter === "done") return t.done;
        return true;
    });

    listEl.innerHTML = "";
    emptyStateEl.hidden = visible.length !== 0;

    for (const task of visible) {
        const li = document.createElement("li");
        li.className = "task-row" + (task.done ? " done" : "");
        li.dataset.id = task.id;

        li.innerHTML = `
            <span class="task-title">${escapeHtml(task.title)}</span>
            <button class="icon-btn complete" title="Toggle complete" data-action="toggle">✓</button>
            <button class="icon-btn remove" title="Delete task" data-action="delete">✕</button>
        `;
        listEl.appendChild(li);
    }
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

formEl.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = inputEl.value.trim();
    if (!title) return;

    await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
    });

    inputEl.value = "";
    await loadTasks();
});

listEl.addEventListener("click", async (e) => {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;

    const row = btn.closest(".task-row");
    const id = row.dataset.id;
    const action = btn.dataset.action;

    if (action === "toggle") {
        const task = cachedTasks.find((t) => t.id == id);
        await fetch(`${API_BASE}/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ done: !task.done }),
        });
    } else if (action === "delete") {
        await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
    }

    await loadTasks();
});

tabButtons.forEach((tab) => {
    tab.addEventListener("click", () => {
        tabButtons.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        currentFilter = tab.dataset.filter;
        render();
    });
});

loadTasks();
