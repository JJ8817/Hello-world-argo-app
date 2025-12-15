{{- define "hello-world.name" -}}
hello-world
{{- end }}

{{- define "hello-world.fullname" -}}
{{ include "hello-world.name" . }}
{{- end }}
