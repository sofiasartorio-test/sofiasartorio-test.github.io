{{/* Questo file viene incluso come JS */}}
const pubs = [
{{- $last := sub (len .Pages) 1 -}}
{{- range $i, $p := .Pages -}}
  {{- $authors := .Params.authors | default (slice "Unknown") -}}
  {{- $types := .Params.publication_types | default (slice "") -}}
  {
    title: {{ .Title | jsonify }},
    authors: {{ $authors | jsonify }},
    year: {{ .Date.Format "2006" | jsonify }},
    type: {{ index $types 0 | default "" | jsonify }},
    url: {{ .RelPermalink | jsonify }}
  }{{ if ne $i $last }},{{ end }}
{{- end -}}
];
