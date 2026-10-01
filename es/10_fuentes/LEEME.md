# Fuentes primarias

Esta carpeta contenía copias locales de los artículos de terceros en los que se apoya el marco. **Se han eliminado del repositorio** porque son material con derechos de autor de sus editoriales y autores.

- La referencia completa de cada fuente (autores, revista, año, DOI/PMID y el dato concreto que aporta) está en `es/red/stasispath.yaml`, sección `fuentes` (F1–F93), y en la bibliografía de los manuscritos.
- Dos scripts de auditoría de `es/20_cotas/` (`auditoria_aristas_tanda49.py`, `cota_campos_lejanos.py`) leían esos PDFs para comprobar frases literales. Para volver a ejecutarlos, obtén los artículos por su DOI y colócalos en `es/10_fuentes/pdf/`. Esa ruta está en `.gitignore`, así que nunca se publicarán por error.
- `fuentes.md` es el índice original de lectura y se conserva.
