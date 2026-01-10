---
title: Publications
cms_exclude: true
view: citation
banner:
  image: ""
  caption: ""
---

<label>Filtra per anno:
  <select id="filtroAnno">
    <option value="">Tutti</option>
  </select>
</label>

<div id="listaPubblicazioni"></div>

<script>
const pubs = [
  {{ range .Pages }}
  {
    title: "{{ .Title | htmlEscape }}",
    authors: "{{ delimit .Params.authors ", " | htmlEscape }}",
    year: {{ .Date.Format "2006" }},
    url: "{{ .RelPermalink }}"
  },
  {{ end }}
];

const anniSet = new Set(pubs.map(p => p.year));
const filtro = document.getElementById("filtroAnno");
Array.from(anniSet).sort((a,b)=>b-a).forEach(y=>{
  const opt = document.createElement("option");
  opt.value = y;
  opt.textContent = y;
  filtro.appendChild(opt);
});

function mostraPubblicazioni() {
  const selezionato = filtro.value;
  const container = document.getElementById("listaPubblicazioni");
  container.innerHTML = "";
  pubs.filter(p => !selezionato || p.year == selezionato)
      .forEach(p=>{
        const div = document.createElement("div");
        div.className = "pub";
        div.innerHTML = `<strong>${p.title}</strong> — ${p.authors} (${p.year}) 
                         <a href="${p.url}">Vai</a>`;
        container.appendChild(div);
      });
}

mostraPubblicazioni();
filtro.addEventListener("change", mostraPubblicazioni);
</script>

<style>
.pub { margin-bottom: 1rem; }
label { font-weight: bold; margin-bottom: 1rem; display: block; }
</style>
