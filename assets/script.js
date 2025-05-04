/* ---------- Utilities ------------------------------------ */
const qs = s => document.querySelector(s);
const $ = s => [...document.querySelectorAll(s)];
const api = (path, body={}) =>
  fetch(path, {method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body)}).then(r => r.json());

/* ---------- State ---------------------------------------- */
const modeKey = "wl_mode", themeKey = "wl_theme";
let mode = localStorage.getItem(modeKey) || "work";
let theme = localStorage.getItem(themeKey) || "dark";
if(theme==="light") document.body.classList.add("light");

/* ---------- Load bookmarks ------------------------------- */
async function load() {
  const res = await fetch(`/data/${mode}.yaml?${Date.now()}`);
  const text = await res.text();
  const data = jsyaml.load(text) || {};
  render(data);
}
function render(data){
  const container = qs("#content");
  container.innerHTML = "";
  for(const [cat,links] of Object.entries(data)){
    const sect = document.createElement("section");
    sect.innerHTML = `<h2>${cat}</h2><div class="cards"></div>`;
    const cards = sect.querySelector(".cards");
    links.forEach(l=>{
      cards.appendChild(cardElem(cat,l));
    });
    const add = document.createElement("div");
    add.className="card add-btn"; add.innerHTML="+";
    add.onclick=()=>openModal("add", {category:cat});
    cards.appendChild(add);
    container.appendChild(sect);
  }
}
/* ---------- Card element --------------------------------- */
function cardElem(category, link){
  const div = document.createElement("div"); div.className="card";
  div.innerHTML = `
    <img src="${link.favicon||'/assets/favicons/default.ico'}" alt="">
    <span>${link.title}</span>
    <button class="menu">⋮</button>`;
  div.onclick = e=>{
    if(e.target.classList.contains("menu")){ e.stopPropagation();
      openModal("edit", {category, link});
    } else window.open(link.url,"_blank");
  };
  return div;
}

/* ---------- Search --------------------------------------- */
qs("#search").addEventListener("input", e=>{
  const q = e.target.value.toLowerCase();
  $(".card").forEach(c=>{
    const txt = c.innerText.toLowerCase();
    c.style.display = txt.includes(q) ? "" : "none";
  });
});

/* ---------- Mode & Theme --------------------------------- */
function setMode(m){ mode=m; localStorage.setItem(modeKey,m); load(); updateTopbar();}
function toggleMode(){ setMode(mode==="work"?"personal":"work");}
function toggleTheme(){
  theme = theme==="dark"?"light":"dark";
  document.body.classList.toggle("light");
  localStorage.setItem(themeKey,theme);
}
function updateTopbar(){
  qs("#title").textContent = mode==="work"?"Work Dashboard":"Personal Dashboard";
  qs("#modeBtn").textContent = mode==="work"?"🏠":"💼";
}
qs("#modeBtn").onclick = toggleMode;
qs("#themeBtn").onclick = toggleTheme;

/* ---------- Modal (add/edit) ----------------------------- */
const modal = qs("#modal");
function openModal(action,ctx){
  modal.dataset.action = action;
  modal.dataset.category = ctx.category;
  if(action==="add"){
    qs("#mTitle").value=""; qs("#mURL").value="";
    qs("#delBtn").style.display="none";
  }else{
    qs("#mTitle").value=ctx.link.title; qs("#mURL").value=ctx.link.url;
    qs("#delBtn").style.display="";
    modal.dataset.origTitle = ctx.link.title;
  }
  modal.classList.add("show");
}
function closeModal(){ modal.classList.remove("show");}
qs("#cancelBtn").onclick = closeModal;
modal.addEventListener("click",e=>{ if(e.target===modal) closeModal();});
qs("#saveBtn").onclick = async ()=>{
  const title = qs("#mTitle").value.trim();
  const url = qs("#mURL").value.trim();
  const category = modal.dataset.category;
  if(!title||!url) return;
  const body = {mode, category, title, url};
  if(modal.dataset.action==="add"){
    await api("/add", body);
  }else{
    body.orig_title = modal.dataset.origTitle;
    await api("/update", body);
  }
  closeModal(); load();
};
qs("#delBtn").onclick = async ()=>{
  await api("/remove", {mode, category:modal.dataset.category, title:modal.dataset.origTitle});
  closeModal(); load();
};

/* ---------- Kick‑off ------------------------------------- */
updateTopbar(); load();
