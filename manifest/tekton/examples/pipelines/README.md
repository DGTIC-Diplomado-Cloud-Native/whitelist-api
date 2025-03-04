## Pipeline CI en Tekton

Esta pipeline realiza las siguientes acciones:
1. Clona el repositorio desde GitHub utilizando la tarea `git-clone`.
2. Construye una imagen de contenedor con `buildah` y la sube a Docker Hub.

### Archivos creados:
- `pipeline-ci.yaml`: Define la pipeline.
- `pipelinerun-ci.yaml`: Ejecuta la pipeline.

Para ejecutarla:
```sh
kubectl create -f pipelinerun-ci.yaml

Para ver los logs:
```sh
tkn pipelinerun logs -f --last