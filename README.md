# 🐜 HormigasAIS Site

## Infraestructura web, PWA y puerta pública del Protocolo LBH

[

![Sitio](https://img.shields.io/badge/HormigasAIS-hormigasais.com-ffd500?style=for-the-badge)

](https://hormigasais.com/)
[

![LBH](https://img.shields.io/badge/Protocol-LBH%20v2.0-00d084?style=for-the-badge)

](https://docs.hormigasais.com/)
[

![License](https://img.shields.io/badge/Code-Apache%202.0-d22128?style=for-the-badge)

](LICENSE)
[

![Security](https://img.shields.io/badge/Security-SECURITY.md-111111?style=for-the-badge)

](SECURITY.md)



![HormigasAIS](https://raw.githubusercontent.com/Thrumanshow/Thrumanshow/main/logo_soberano_hd.png)



> **HormigasAIS** es una infraestructura de inteligencia distribuida orientada al borde, con software, protocolo LBH, SDKs, documentación y nodos operados desde San Miguel, El Salvador.

Este repositorio es el **centro web funcional** del ecosistema HormigasAIS. Reúne el sitio público, la PWA, recursos de identidad, componentes de integración y la conexión documental con la API y los nodos Edge.

## Enlaces principales

| Recurso | Enlace | Función |
|---|---|---|
| Sitio | [hormigasais.com](https://hormigasais.com/) | Plataforma pública, servicios y planes. |
| Documentación | [docs.hormigasais.com](https://docs.hormigasais.com/) | Protocolo LBH, API, manual y SDKs. |
| Legal | [Marco legal](https://docs.hormigasais.com/legal.html) | Privacidad, términos y propiedad intelectual. |
| Blog | [blog.hormigasais.com](https://blog.hormigasais.com/) | Bitácora y publicaciones técnicas. |
| Financiación | [GitHub Sponsors](https://github.com/sponsors/Thrumanshow) | Apoyo al desarrollo abierto. |

## Arquitectura

    hormigasais.com       Sitio · PWA · servicios
            │
            ├── docs.hormigasais.com   LBH · API · SDK · legal
            ├── blog.hormigasais.com    Publicaciones y bitácora
            └── api.hormigasais.com     Integración del nodo Edge
                        │
              Nodo A16 · Termux · Linux

SDKs: Python · JavaScript/Node.js
Integración opcional: Discord Ant Bot

## Componentes relacionados

| Proyecto | Papel |
|---|---|
| hormigasais-foundation | Base institucional, arquitectura y evidencia. |
| hormigasais-edge-starter | Plantilla y laboratorio para nodos Edge/Termux. |
| lbh-sdk · PyPI | SDK oficial Python del protocolo LBH. |
| lbh-sdk-hormigasais · npm | SDK oficial JavaScript/Node.js. |
| discord-ant-bot | Integración opcional mediante Discord. |

## Protocolo, identidad y evidencia

El Protocolo LBH define el lenguaje de integridad e intercambio utilizado por los componentes del ecosistema. Consulta la documentación LBH y el SDK Ecosystem.

La clave `.human`, presente en la configuración de la PWA, se considera un metadato de identidad de interfaz. No es una licencia ni un estándar legal por sí mismo.

La documentación institucional menciona MESENTERY v1.0 como especificación o licencia institucional. Hasta que exista un texto canónico versionado con sus términos, MESENTERY no debe interpretarse como sustituto de la licencia del código.

Como evidencia versionada, consulta Zenodo 10.5281/zenodo.17767205 y Zenodo 10.5281/zenodo.19177759. Los DOI documentan publicaciones concretas y no sustituyen el LICENSE de este repositorio.

## Licencia y seguridad

El código cubierto por este repositorio se distribuye bajo la Apache License 2.0. La licencia permite uso, modificación y distribución conforme a sus condiciones. No concede automáticamente derechos sobre las marcas, logos, nombres comerciales, datos, servicios de pago o contenido de terceros.

La política de seguridad está en SECURITY.md. Nunca publiques NODE_SECRET, tokens, claves privadas, contraseñas ni credenciales de producción. Las variables sensibles deben cargarse desde el entorno o un gestor de secretos. Si un secreto aparece en Git, debe rotarse y auditarse el historial.

## Financiación

GitHub Sponsors está configurado mediante .github/FUNDING.yml. PayPal se conserva en hormigasais.com como canal comercial de los planes publicados. Son funciones distintas: Sponsors financia el desarrollo; PayPal gestiona operaciones comerciales.

## Estado

hormigasais-site es la capa web central de HormigasAIS y un proyecto en evolución. La arquitectura, documentación, API, PWA, SDKs y evidencia deben mantenerse sincronizados mediante versiones y pruebas.

## Autoría

Cristhiam Leonardo Hernández Quiñonez (CLHQ)
Fundador de HormigasAIS · Nodo A16 · San Miguel, El Salvador

## Documento de arquitectura visual

Para una explicación gráfica de la separación de responsabilidades entre el sitio, la base institucional, los nodos Edge, los SDKs y las integraciones periféricas, consulta el documento oficial de diseño:

- **[Descargar Arquitectura Modular de HormigasAIS (PDF)](../docs/assets/hormigasais-arquitectura-modular.pdf)**

Este documento complementa la especificación técnica, la política de seguridad (`SECURITY.md`) y el marco legal del ecosistema, sirviendo como evidencia visual de la infraestructura soberana bajo el principio: *"Una función, un repositorio, una responsabilidad"*.
