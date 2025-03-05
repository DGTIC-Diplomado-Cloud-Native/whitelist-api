# Estrategia de Ramificación

## Estructura Principal

```
main (producción)
└── develop (desarrollo)
    ├── feature/* (funcionalidades)
    ├── bugfix/* (correcciones)
    └── release/* (versiones)
```

## Ramas Permanentes

### main
- Contiene código en producción
- Solo recibe merges desde release/* o hotfix/*
- Cada merge genera un tag de versión
- Protegida: requiere PR y 2 aprobaciones

### develop
- Rama principal de desarrollo
- Integra todas las funcionalidades completadas
- Base para nuevas features
- Requiere 1 aprobación para PR

## Ramas Temporales

### feature/*
- Formato: feature/[ticket-id]-breve-descripcion
- Creada desde: develop
- Merge hacia: develop
- Para nuevas funcionalidades
- Una rama por ticket/tarea

### bugfix/*
- Formato: bugfix/[ticket-id]-descripcion-error
- Creada desde: develop
- Merge hacia: develop
- Para correcciones en desarrollo

### release/*
- Formato: release/v[major].[minor].[patch]
- Creada desde: develop
- Merge hacia: main y develop
- Para preparar nuevas versiones
- Solo correcciones menores permitidas

### hotfix/*
- Formato: hotfix/[ticket-id]-descripcion
- Creada desde: main
- Merge hacia: main y develop
- Para correcciones urgentes en producción

## Flujo de Trabajo

1. Desarrollador crea feature/* o bugfix/* desde develop
2. Trabaja en cambios con commits frecuentes
3. Abre PR cuando completa la tarea
4. Obtiene revisiones necesarias
5. Merge a develop tras aprobación
6. Release manager crea release/* para versiones
7. Pruebas finales en rama release
8. Merge a main y develop tras validación

## Convenciones de Commits

```
<tipo>(<alcance>): <descripción>

[cuerpo]

[pie]
```

Tipos:
- feat: nueva funcionalidad
- fix: corrección de error
- docs: documentación
- style: formato
- refactor: restructuración de código
- test: pruebas
- chore: mantenimiento

## Roles y Responsabilidades

- Release Manager: gestiona releases y hotfixes
- Tech Lead: aprueba PRs a main
- Desarrolladores: crean features y bugfixes
- QA: valida releases antes de producción

## Herramientas Recomendadas

- GitHub Actions para CI/CD
- Branch protection rules
- PR templates
- Conventional commits lint
- Semantic versioning

## Pipeline
Actual: 5
