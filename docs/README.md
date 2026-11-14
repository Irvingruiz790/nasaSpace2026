# `docs/` — documentación del equipo

**Dueño:** todos, con aviso en el chat antes de editar.
**Documento que manda:** `Guia_Equipo.docx`.

---

## Qué va aquí

| Archivo | Para qué | Formato |
|---|---|---|
| `Guia_Equipo.docx` | **Documento único de trabajo diario.** Paso a paso por equipo. | Word (.docx) |
| `CONTRATO_DATOS.md` | Nombres y significado de cada campo del dataset | Markdown |
| `DECISIONES.md` | Registro de decisiones del equipo, con fecha y motivo | Markdown |
| `FUENTES.md` | Protocolo para verificar datos y citar fuentes | Markdown |
| `PITCH.md` | Guion y estructura del pitch de 2 minutos | Markdown |

## Regla de prioridad

Si la guía Word dice una cosa y un documento largo dice otra, **manda la guía
Word**. Los `.md` son consulta técnica.

## Cómo se actualiza la guía

La guía no se edita a mano: se regenera desde
`scripts/generar_guia_word.py`.

```powershell
.\.venv\Scripts\python.exe scripts\generar_guia_word.py
```

Si cambia el plan, primero se actualiza el script y después se regenera el
`.docx`, para que ambos digan lo mismo.

## Reglas

- Un cambio de decisión se anota en `DECISIONES.md` con fecha, quién y por qué.
- No se suben borradores con nombre personal (`guia-final-v2-ahora-si.docx`).
- No se sube el archivo temporal de Word (`~$...docx`): está en `.gitignore`.
- Los documentos se escriben en español, con frases cortas.
