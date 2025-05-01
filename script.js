
const CATEGORIES = ['Chats', 'Dashboards', 'Docs', 'Tools'];

function loadLinks(filter = "") {
  fetch('/data.yaml')
    .then(response => response.text())
    .then(text => jsyaml.load(text))
    .then(data => {
      CATEGORIES.forEach(category => {
        const container = document.getElementById(category);
        container.innerHTML = "";
        const links = (data[category] || []).filter(link =>
          link.title.toLowerCase().includes(filter.toLowerCase()) ||
          link.url.toLowerCase().includes(filter.toLowerCase())
        );
        links.forEach((link, index) => {
          const card = createCard(link.title, link.url, link.favicon, category, index);
          container.appendChild(card);
        });
      });
    });
}

function createCard(title, url, favicon, category, index) {
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `
    <div class="top">
      <a href="${url}" target="_blank" class="title">
        <img src="${favicon}" />
        <strong>${title}</strong>
      </a>
      <button onclick="openEditor('${category}', ${index})">⋮</button>
    </div>
  `;
  return card;
}

function openEditor(category, index) {
  fetch('/data.yaml')
    .then(response => response.text())
    .then(text => jsyaml.load(text))
    .then(data => {
      const link = data[category][index];
      const editor = document.getElementById("editor");
      editor.innerHTML = `
        <h3>Edit Card</h3>
        <label>Title:</label>
        <input id="editTitle" value="${link.title}" />
        <label>URL:</label>
        <input id="editUrl" value="${link.url}" />
        <button onclick="saveChanges('${category}', ${index})">💾 Save</button>
        <button onclick="removeLink('${category}', ${index})">🗑️ Delete</button>
        <button onclick="closeEditor()">❌ Cancel</button>
      `;
      editor.style.display = "block";
    });
}

function closeEditor() {
  document.getElementById("editor").style.display = "none";
}

function saveChanges(category, index) {
  const title = document.getElementById("editTitle").value;
  const url = document.getElementById("editUrl").value;
  fetchFavicon(url).then(favicon => {
    Promise.all([
      fetch('/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, index, field: 'title', value: title })
      }),
      fetch('/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, index, field: 'url', value: url })
      }),
      fetch('/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, index, field: 'favicon', value: favicon })
      })
    ]).then(() => {
      closeEditor();
      loadLinks(document.getElementById("searchBar").value);
    });
  });
}

function addLink(category) {
  const title = prompt("Enter title:");
  const url = prompt("Enter URL (include https://):");
  if (!title || !url) return;

  fetchFavicon(url).then(favicon => {
    fetch('/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category, title, url, favicon })
    }).then(() => loadLinks(document.getElementById("searchBar").value));
  });
}

function removeLink(category, index) {
  fetch('/remove', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ category, index })
  }).then(() => {
    closeEditor();
    loadLinks(document.getElementById("searchBar").value);
  });
}

async function fetchFavicon(url) {
  try {
    const domain = new URL(url).origin;
    const response = await fetch(`/fetch_favicon?url=${encodeURIComponent(domain)}`);
    const result = await response.json();
    return result.favicon || "/default.ico";
  } catch (e) {
    return "/default.ico";
  }
}

window.onload = () => {
  const searchInput = document.getElementById("searchBar");
  searchInput.addEventListener("input", () => loadLinks(searchInput.value));
  loadLinks();
};
