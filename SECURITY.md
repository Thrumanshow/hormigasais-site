# Política de Seguridad

## Reportar una vulnerabilidad

Si encuentras una vulnerabilidad de seguridad en este repositorio o en la infraestructura de HormigasAIS, repórtala de forma privada a:

**clhq@hormigasais.com** — asunto: "Seguridad"

No abras un issue público para vulnerabilidades sin confirmar antes. Se atienden reportes en un plazo razonable dado que este es un proyecto mantenido por una sola persona.

## Qué nunca debe aparecer en este repositorio

- `NODE_SECRET`, `LBH_SECRET`, `MASTER_SEAL_KEY` u otras claves de firma
- Tokens de API (GitHub, Cloudflare, npm, PyPI)
- Claves privadas SSH o certificados
- Archivos `.env` con valores reales
- Credenciales de bases de datos

Las variables sensibles se cargan desde el entorno (`os.environ.get(...)` en Python, `process.env` en Node) o desde un gestor de secretos local, nunca hardcodeadas en el código fuente.

## Si un secreto se filtra

1. Rotar la credencial afectada de inmediato en el servicio correspondiente.
2. Eliminar el valor del código fuente y sustituirlo por una variable de entorno.
3. Si el secreto quedó en el historial de Git, evaluar limpieza del historial además de la rotación.

## Alcance

Esta política cubre el código de este repositorio (`hormigasais-site`) y su despliegue en `hormigasais.com`. Para otros repositorios del ecosistema HormigasAIS, cada uno mantiene su propia política si aplica.
