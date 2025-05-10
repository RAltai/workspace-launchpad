const qs = sel => document.querySelector(sel);
const $$ = sel => [...document.querySelectorAll(sel)];
const api = (path, body = {}) =>
  fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  }).then(r => r.json());

const MODE_KEY = "wl_mode";
const THEME_KEY = "wl_theme";
const VALID_MODES = ["work", "personal"];

let mode = VALID_MODES.includes(localStorage.getItem(MODE_KEY))
  ? localStorage.getItem(MODE_KEY)
  : "work";
let theme = localStorage.getItem(THEME_KEY) || "dark";

localStorage.setItem(MODE_KEY, mode);
if (theme === "light") document.body.classList.add("light");

async function load() {
  const res = await fetch(`/data/${mode}.yaml?${Date.now()}`);
  const text = await res.text();
  const data = jsyaml.load(text) || {};
  render(data);
  setupDragAndDrop();
}

function render(data) {
  const container = qs("#content");
  container.innerHTML = "";

  for (const [category, links = []] of Object.entries(data)) {
    const sect = document.createElement("section");
    sect.innerHTML = `
      <h2>
        ${category}
        <button class="cat-del" title="Delete category">🗑</button>
      </h2>
      <div class="link-list" data-category="${category}">
        <div class="cards"></div>
      </div>`;

    sect.querySelector(".cat-del").onclick = async e => {
      e.stopPropagation();
      if (!confirm(`Delete entire category “${category}”?`)) return;
      await api("/delete_category", { mode, category });
      load();
    };

    const cards = sect.querySelector(".cards");

    links.forEach(link => cards.appendChild(cardElem(category, link)));

    const add = document.createElement("div");
    add.className = "card add-btn";
    add.textContent = "+";
    add.onclick = () => openModal("add", { category });
    cards.appendChild(add);

    container.appendChild(sect);
  }
}

function cardElem(category, link) {
  const div = document.createElement("div");
  div.className = "card";
  div.innerHTML = `
    <img src="${link.favicon || '/assets/favicons/default.ico'}" alt="">
    <span>${link.title}</span>
    <button class="menu">⋮</button>`;

  div.onclick = e => {
    if (e.target.classList.contains("menu")) {
      e.stopPropagation();
      openModal("edit", { category, link });
    } else {
      window.location.href = link.url;
    }
  };
  return div;
}

qs("#search").addEventListener("input", e => {
  const q = e.target.value.toLowerCase();
  $$(".card").forEach(card => {
    const txt = card.innerText.toLowerCase();
    card.style.display = txt.includes(q) ? "" : "none";
  });
});

function setMode(m) {
  mode = m; localStorage.setItem(MODE_KEY, m);
  load(); updateTopbar();
}
function toggleMode() { setMode(mode === "work" ? "personal" : "work"); }
function toggleTheme() {
  theme = theme === "dark" ? "light" : "dark";
  document.body.classList.toggle("light");
  localStorage.setItem(THEME_KEY, theme);
}
function updateTopbar() {
  qs("#title").textContent = mode === "work" ? "Work Dashboard"
    : "Personal Dashboard";
  qs("#modeBtn").textContent = mode === "work" ? "🏠" : "💼";
}
qs("#modeBtn").onclick = toggleMode;
qs("#themeBtn").onclick = toggleTheme;

const modal = qs("#modal");

function openModal(action, ctx) {
  modal.dataset.action = action;
  modal.dataset.category = ctx.category;
  modal.dataset.origTitle = ctx.link?.title || "";

  qs("#mTitle").value = ctx.link?.title || "";
  qs("#mURL").value = ctx.link?.url || "";
  qs("#delBtn").style.display = action === "add" ? "none" : "";

  modal.classList.add("show");
}
function closeModal() { modal.classList.remove("show"); }
qs("#cancelBtn").onclick = closeModal;
modal.onclick = e => { if (e.target === modal) closeModal(); };

qs("#saveBtn").onclick = async () => {
  const title = qs("#mTitle").value.trim();
  const url = qs("#mURL").value.trim();
  if (!title || !url) return;

  const body = { mode, category: modal.dataset.category, title, url };

  if (modal.dataset.action === "add") {
    await api("/add", body);
  } else {
    body.orig_title = modal.dataset.origTitle;
    await api("/update", body);
  }
  closeModal(); load();
};
qs("#delBtn").onclick = async () => {
  await api("/remove", {
    mode,
    category: modal.dataset.category,
    title: modal.dataset.origTitle
  });
  closeModal(); load();
};

const catModal = qs("#catModal");
qs("#newCatBtn").onclick = () => { qs("#catName").value = ""; catModal.classList.add("show"); };
qs("#catCancel").onclick = () => catModal.classList.remove("show");
qs("#catSave").onclick = async () => {
  const name = qs("#catName").value.trim();
  if (!name) return;
  await api("/add_category", { mode, category: name });
  catModal.classList.remove("show");
  load();
};

qs("#importYamlBtn").onclick = () => qs("#importYamlFile").click();

qs("#importYamlFile").addEventListener("change", async e => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`/import_yaml?mode=${mode}`, { method: "POST", body: formData });
  alert(res.ok ? "Import successful!" : `Import failed: ${(await res.json()).error}`);
  if (res.ok) load();
});

qs("#exportYamlBtn").onclick = () => {
  window.location.href = `/export_yaml?mode=${mode}`;
};

function setupDragAndDrop() {
  $$(".cards").forEach(el => {
    const category = el.closest(".link-list")?.dataset.category;
    if (!category) return;

    new Sortable(el, {
      group: "shared-links",
      animation: 150,
      ghostClass: "drag-ghost",
      onEnd: async evt => {
        const fromCat = evt.from.closest(".link-list")?.dataset.category;
        const toCat = evt.to.closest(".link-list")?.dataset.category;
        if (!fromCat || !toCat) return;

        if (fromCat === toCat && evt.oldIndex === evt.newIndex) return;

        await api("/move_link", {
          mode,
          from_category: fromCat,
          to_category: toCat,
          old_index: evt.oldIndex,
          new_index: evt.newIndex
        });
        load();
      }
    });
  });
}

updateTopbar();
load();
