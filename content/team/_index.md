---
title: "👥 Our Team"
weight: 2
disable_toc: true
no_sidebar: true
headless: false
---

<div class="people-grid">
{{ range (where site.RegularPages "Section" "authors") }}
  <div class="person-card">
    {{ $avatar := .Params.avatar | default "/images/default-avatar.png" }}
    <img class="avatar" src="{{ $avatar }}" alt="{{ .Title }}">

    <h3>{{ .Title }}</h3>

    {{ if .Params.role }}
      <p class="role">{{ .Params.role }}</p>
    {{ end }}

    <div class="socials">
      {{ with .Params.social }}
        {{ if .email }}<a href="mailto:{{ .email }}">Email</a>{{ end }}
        {{ if .scholar }} | <a href="{{ .scholar }}">Google Scholar</a>{{ end }}
      {{ end }}
    </div>
  </div>
{{ end }}
</div>

<style>
.people-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 2rem;
  justify-items: center;
  margin-top: 2rem;
}
.person-card { text-align: center; }
.avatar { width: 150px; height: 150px; object-fit: cover; border-radius: 50%; }
.role { font-size: 0.9rem; color: #555; }
.socials a { margin: 0 0.5rem; font-size: 0.9rem; color: #007acc; text-decoration: none; }
</style>


