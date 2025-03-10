# WhiteIAList - API de Reconocimiento Facial de Superhéroes

![Avengers Logo](https://i.imgur.com/example-avengers-logo.png)

## ¿De qué trata mi proyecto?

¡He creado una API súper cool que básicamente funciona como un "detector de Vengadores"! 😄 Mi API utiliza el poder de reconocimiento facial de AWS Rekognition para determinar si alguien es parte del equipo de superhéroes o no.

## ¿Qué hace exactamente?

En pocas palabras, he construido una "lista blanca" (whitelist) de rostros de los Vengadores utilizando AWS Rekognition Collections. Cuando alguien envía una foto, mi API puede decir "Sí, es Thor" o "Lo siento, este tipo no es un Vengador" basándose en el reconocimiento facial.

## Mis endpoints principales:

### 1. Mi Detector de Vengadores 🦸

- **Ruta**: `/collections/search-in-collection/`
- **Método**: POST
- **¿Qué hace?**: Recibe una URL de imagen (por ejemplo, una foto de Mark Ruffalo) y compara ese rostro con mi colección "avengers-whitelist". Si hay coincidencia, devuelve detalles como el ID, nivel de confianza, etc.
- **Ejemplo de uso**: Envías la URL de una imagen de Bruce Banner y mi API te responde básicamente "Sí, es Hulk, confío en ello un 95%"

### 2. Registro de Usuarios

- **Ruta**: `/users/sing-up/` (¡ojo con el typo en "sign"!)
- **Método**: POST
- **¿Qué hace?**: Permite registrar usuarios con email, teléfono y contraseña (con validaciones de seguridad)

### 3. Salud de la API

- **Ruta**: `/`
- **Método**: GET
- **¿Qué hace?**: Un simple endpoint para verificar que mi API está funcionando correctamente (devuelve `{"status": "Health"}`)

### 4. Lista de Colecciones

- **Ruta**: `/collections/list-collections`
- **Método**: GET
- **¿Qué hace?**: Te muestra todas las colecciones de rostros que tengo actualmente en AWS Rekognition.

## Cómo funciona bajo el capó

Mi API está utilizando FastAPI (¡buena elección!) y está construida con una arquitectura bastante limpia:

- **MongoDB** para almacenar los usuarios
- **AWS Rekognition** para toda la magia del reconocimiento facial
- **Docker** para empaquetar todo lindo y portátil
- **Tekton** para CI/CD (estoy preparado para despliegue continuo en Kubernetes/OpenShift)

Cuando alguien sube una foto, mi servicio `CollectionsService` se comunica con AWS, hace la magia del reconocimiento facial, y devuelve un resultado en forma de: "Sí, este rostro coincide con [nombre del vengador] con una confianza del XX%".

## Demostración

Los rostros almacenados previamente en la whitelist son los de los vengadores:

![Avengers Team](https://i.imgur.com/example-avengers-image.png)

Cualquier rostro que no coincida con alguno de estos super héroes, será rechazado.

Si damos un vistazo a la documentación de la API, veremos que hay un endpoint que recibe una url de una imagen pública en la Web y nos dice si tiene coincidencias de rostros. En otras palabras, si la imagen que pasamos tiene algún rostro de un vengador, nos dice cual de ellos se encontró.

Desafortunadamente aún estoy en lista de espera para unirme a los vengadores, mientras eso pasa, si yo envío una foto mía como parámetro en el endpoint de la API, el resultado es:

```
https://avatars.githubusercontent.com/u/14140450?v=4
```

En caso contrario si paso una imagen de Iron Man como parámetro, el resultado es una respuesta positiva.

## Código del Proyecto y Manifiestos

A continuación se proporciona el repositorio con el código del proyecto, donde se encuentran los manifiestos necesarios:

```
https://github.com/DGTIC-Diplomado-Cloud-Native/whitelist-api.git
```

## Plan de Implementación para el Pipeline de Tekton

Después de analizar los manifiestos proporcionados, implementaré una solución que sigue el flujo de CI/CD completo, desde la configuración de permisos necesarios hasta la ejecución del pipeline.

### 1. Creación de Namespaces y Workspaces

Primero, necesitamos asegurarnos de que tenemos el namespace correcto y el espacio de trabajo persistente para nuestros pipelines:

```bash
# Primero verifico si el namespace ya existe
kubectl get namespace diploe2-lunafelipe1997 || kubectl create namespace diploe2-lunafelipe1997
# Aplico el PersistentVolumeClaim para tener almacenamiento para nuestros pipelines
kubectl apply -f manifest/tekton/workspaces/workspace-pvc.yaml
```

Este paso es fundamental porque:
- El namespace `diploe2-lunafelipe1997` aísla nuestros recursos de Tekton del resto del clúster, proporcionando un entorno dedicado y seguro.
- El PersistentVolumeClaim crea un volumen de almacenamiento persistente donde los pipelines de Tekton pueden clonar repositorios y compartir archivos entre tareas, lo que es esencial para mantener la consistencia entre las diferentes etapas del pipeline.

### 2. Configuración de Permisos y Service Accounts

A continuación, necesito configurar los permisos necesarios para que Tekton pueda interactuar con Kubernetes:

```bash
# Aplico primero los service accounts
kubectl apply -f manifest/tekton/rbac/service-accounts/general-service-account.yaml
kubectl apply -f manifest/tekton/rbac/service-accounts/triggers-service-account.yaml
# Luego aplico los roles
kubectl apply -f manifest/tekton/rbac/permissions/roles/general-role.yaml
kubectl apply -f manifest/tekton/rbac/permissions/roles/triggers-resources-role.yaml
kubectl apply -f manifest/tekton/rbac/permissions/clouster-roles/triggers-interceptors-clusterrole.yaml
# Finalmente, aplico los role bindings
kubectl apply -f manifest/tekton/rbac/permissions/role-bindings/general-role-binding.yaml
kubectl apply -f manifest/tekton/rbac/permissions/role-bindings/triggers-resources-role-binding.yaml
kubectl apply -f manifest/tekton/rbac/permissions/role-bindings/triggers-role-binding.yaml
kubectl apply -f manifest/tekton/rbac/permissions/clouster-role-bindings/triggers-interceptors-clusterrolebinding.yaml
```

Esta configuración de RBAC (Control de Acceso Basado en Roles) es crucial porque:

1. **Service Accounts**: Son identidades con las que Tekton opera en Kubernetes.
   - `general-service-account.yaml` crea el usuario `tekton-sa` que utilizará nuestro pipeline principal.
   - `triggers-service-account.yaml` crea el usuario `tekton-triggers-sa` específico para los triggers de eventos.

2. **Roles y ClusterRoles**: Definen los permisos específicos.
   - `general-role.yaml` otorga permisos para gestionar pods, secretos, configuraciones y recursos de Tekton.
   - `triggers-resources-role.yaml` otorga permisos específicos para trabajar con los recursos de Tekton Triggers.
   - `triggers-interceptors-clusterrole.yaml` define permisos a nivel de clúster para interceptar eventos.

3. **RoleBindings y ClusterRoleBindings**: Asignan los roles a los service accounts.
   - Conectan nuestras cuentas de servicio con los permisos que necesitan para funcionar correctamente.

Sin esta configuración, los componentes de Tekton no podrían crear pods, acceder a secretos o gestionar recursos de Kubernetes, lo que haría imposible la ejecución del pipeline.

### 3. Creación de Secretos

Ahora, necesito configurar los secretos necesarios para acceder a Docker Hub y AWS:

```bash
# Primero, debo crear el secret para Docker Hub para poder subir la imagen
# Nota: Necesito reemplazar la plantilla con el base64 correcto antes de aplicarlo
kubectl apply -f manifest/tekton/secrets/docker-secret.yaml
# Luego, configuro los secretos para AWS
# Nota: Necesito reemplazar los valores de plantilla con los valores reales de AWS
kubectl apply -f manifest/tekton/secrets/aws-secret.yaml
```

Los secretos son fundamentales en nuestro pipeline porque:

1. **Docker Hub Secret**: Permite a Tekton autenticarse con Docker Hub para poder subir las imágenes construidas. Sin esta autenticación, la etapa de push en nuestro pipeline fallaría.

2. **AWS Secret**: Proporciona las credenciales necesarias para que la aplicación se conecte con los servicios de AWS Rekognition. Aunque no se usa directamente en el pipeline, es un requisito para que la aplicación desplegada funcione correctamente.

Estos secretos permiten mantener nuestras credenciales sensibles fuera del código y los manifiestos, siguiendo las mejores prácticas de seguridad.

### 4. Instalación de Tareas Reutilizables

Tekton utiliza tareas reutilizables para operaciones comunes. Necesito asegurarme de que están instaladas:

```bash
# Instalo la tarea git-clone desde el catálogo de tareas de Tekton
kubectl apply -f https://raw.githubusercontent.com/tektoncd/catalog/main/task/git-clone/0.5/git-clone.yaml
# Instalo la tarea buildah para construir imágenes de Docker
kubectl apply -f https://raw.githubusercontent.com/tektoncd/catalog/main/task/buildah/0.4/buildah.yaml
# Aplico la tarea kubectl-apply personalizada
kubectl apply -f manifest/tekton/tasks/kubectl-apply.yaml
```

Estas tareas son componentes esenciales del pipeline porque:

1. **git-clone**: Proporciona la capacidad de clonar repositorios Git, lo que es el primer paso en cualquier pipeline CI/CD. Esta tarea maneja automáticamente la clonación superficial, la gestión de credenciales y otras optimizaciones.

2. **buildah**: Permite construir imágenes de contenedor sin necesidad de un daemon Docker, lo que es más seguro y eficiente en entornos de Kubernetes. Utilizando esta tarea, podemos construir nuestra imagen en un entorno aislado.

3. **kubectl-apply**: Es una tarea personalizada que te permite desplegar recursos en Kubernetes. Esta tarea es particularmente importante porque conecta la parte de CI (construcción de la imagen) con la parte de CD (despliegue de la aplicación).

### 5. Definición del Pipeline

Ahora, puedo aplicar la definición del pipeline principal:

```bash
kubectl apply -f manifest/tekton/pipelines/pipeline.yaml
```

Este archivo es el corazón de nuestra automatización y define un flujo completo de CI/CD que:

1. Clona el repositorio utilizando la tarea git-clone.
2. Construye la imagen de Docker utilizando buildah.
3. Despliega la aplicación utilizando kubectl-apply.

La estructura del pipeline está diseñada para ser modular y parametrizable, lo que permite reutilizarlo con diferentes repositorios, ramas y configuraciones de despliegue. Los workspaces definidos facilitan el compartir datos entre las diferentes tareas.

Es importante notar que este pipeline sigue el principio de "Infrastructure as Code", donde todo el proceso de construcción y despliegue está definido declarativamente, lo que facilita la reproducibilidad y el control de versiones.

### 6. Configuración de Triggers (Opcional)

Si quiero que el pipeline se ejecute automáticamente en respuesta a eventos (como push a Git), debo configurar los triggers:

```bash
# Aplico el TriggerBinding
kubectl apply -f manifest/tekton/triggers/trigger-binding.yaml
# Aplico el TriggerTemplate
kubectl apply -f manifest/tekton/triggers/trigger-template.yaml
# Aplico el EventListener
kubectl apply -f manifest/tekton/triggers/event-listener.yaml
# Configurar el Ingress para hacer accesible el EventListener desde fuera del clúster
kubectl apply -f manifest/tekton/triggers/ingress.yaml
```

Esta configuración de triggers es importante porque:

1. **TriggerBinding**: Define cómo extraer parámetros de los eventos (por ejemplo, la URL del repositorio o la rama) y mapearlos a los parámetros del pipeline.

2. **TriggerTemplate**: Define qué recursos crear cuando se active un trigger, en este caso un PipelineRun.

3. **EventListener**: Crea un endpoint HTTP que escucha eventos externos (como webhooks de GitHub) y los procesa utilizando los TriggerBindings y TriggerTemplates.

4. **Ingress**: Expone el EventListener fuera del clúster, permitiendo que servicios externos como GitHub puedan enviar eventos.

Con esta configuración, habilito un flujo de trabajo completamente automatizado donde cada push a la rama principal dispara automáticamente el pipeline.

### 7. Aplicación del Deployment

Antes de configurar los triggers o ejecutar el pipeline, necesitamos aplicar el archivo de deployment para que Kubernetes sepa cómo debe desplegarse nuestra aplicación:

```bash
# Aplico el deployment de la aplicación
kubectl apply -f manifest/tekton/deployments/whitelist-api-deployment.yaml
# Aplico el servicio que expondrá la aplicación
kubectl apply -f manifest/tekton/services/whitelist-api-service.yaml
```

Este paso es fundamental porque:

1. El archivo de deployment (`whitelist-api-deployment.yaml`) define la configuración exacta de cómo debe ejecutarse nuestra aplicación en Kubernetes:
   - Indica que queremos 1 réplica de nuestro contenedor
   - Especifica la imagen Docker que debe utilizarse (`docker.io/aluna1997/whitelist-api:3.0`)
   - Define los recursos necesarios (CPU y memoria)
   - Configura las variables de entorno que la aplicación necesita, como la conexión a MongoDB y las credenciales de AWS
   - Establece el puerto donde la aplicación escuchará (8000)

2. El archivo de servicio (`whitelist-api-service.yaml`) crea un punto de acceso estable para nuestra aplicación:
   - Define un nombre DNS interno (`whitelist-api-service`) que otros servicios pueden usar para comunicarse con nuestra API
   - Mapea el puerto del servicio (8000) al puerto del contenedor (8000)
   - Utiliza selectores para identificar a qué pods debe dirigir el tráfico (`app: whitelist-api`)

### 8. Ejecución Automática del Pipeline mediante GitHub

Para habilitar la ejecución automática del pipeline cuando se realiza un push a la rama main de GitHub, necesito realizar los siguientes pasos:

```bash
# 1. Asegurarme de que los componentes de Triggers están correctamente configurados
kubectl get eventlistener event-listener-cicd -n diploe2-lunafelipe1997
kubectl get svc el-event-listener-cicd -n diploe2-lunafelipe1997
kubectl get ingress ingress-el -n diploe2-lunafelipe1997

# 2. Obtener la URL completa del EventListener
echo "URL del Webhook: http://el-event-listener-cicd.142326f7-9998-4329-b..."
```

Ahora, debo configurar un webhook en mi repositorio de GitHub:

1. Voy al repositorio GitHub: https://github.com/DGTIC-Diplomado-Cloud-Native/whitelist-api
2. Accedo a "Settings" → "Webhooks" → "Add webhook"
3. Configuro el webhook con los siguientes valores:
   - **Payload URL**: La URL del EventListener obtenida anteriormente
   - **Content type**: application/json
   - **Secret**: Puedo definir un secret opcional para mayor seguridad
   - **Events to trigger**: Selecciono "Just the push event"
   - **Active**: Marco esta casilla para activar el webhook

Esta configuración es crucial porque establece un puente directo entre GitHub y nuestro cluster de Kubernetes. Cuando un desarrollador hace push a la rama main, GitHub envía inmediatamente un evento HTTP POST a nuestro EventListener, que contiene toda la información relevante sobre el commit:
- Quién realizó el cambio
- Qué archivos fueron modificados
- El mensaje del commit
- La URL del repositorio
- El hash del commit

Nuestro TriggerBinding (aplicado en el paso 6) está configurado para extraer específicamente:
- La URL del repositorio desde `$(body.repository.clone_url)`
- El hash del commit desde `$(body.head_commit.id)` para etiquetar nuestra imagen de manera única

### 9. Verificación y Monitoreo

Después de iniciar el pipeline, necesito verificar su progreso y asegurarme de que todas las etapas se completan correctamente:

```bash
# Ver todos los PipelineRuns
kubectl get pipelineruns -n diploe2-lunafelipe1997

# Obtener detalles de un PipelineRun específico (reemplazar con el nombre real)
kubectl describe pipelinerun {{name}} -n diploe2-lunafelipe1997

# Ver los pods creados por el pipeline
kubectl get pods -n diploe2-lunafelipe1997

# Ver los logs de un TaskRun específico
kubectl logs -l tekton.dev/taskRun=manual-run-12345-git-clone -n diploe2-lunafelipe1997 -f
```

Para verificar que el despliegue fue exitoso, debo comprobar:

1. **Deployment**: Verificar que el deployment se haya creado y esté en estado "Ready".
```bash
kubectl get deployment whitelist-api-deployment -n diploe2-lunafelipe1997
```

2. **Pods**: Verificar que los pods del deployment estén en estado "Running".
```bash
kubectl get pods -l app=whitelist-api -n diploe2-lunafelipe1997
```

3. **Servicio**: Verificar que el servicio esté correctamente configurado.
```bash
kubectl get service whitelist-api-service -n diploe2-lunafelipe1997
```

4. **Prueba funcional**: Realizar una solicitud HTTP para verificar que la API responde correctamente.
```bash
# Si el servicio está expuesto a través de un NodePort o LoadBalancer
curl http://[SERVICE-IP]:[PORT]/v1/

# O usar port-forwarding
kubectl port-forward svc/whitelist-api-service 8000:8000 -n diploe2-lunafelipe1997
curl http://localhost:8000/v1/
```

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

## Consideraciones Finales y Explicación del Pipeline

El flujo completo funciona de la siguiente manera:

1. Un desarrollador hace push a la rama main
2. GitHub envía un evento webhook a nuestro EventListener
3. El EventListener procesa el evento a través del interceptor de GitHub, que valida que sea un evento push legítimo
4. El TriggerBinding extrae los parámetros relevantes del evento
5. El TriggerTemplate crea un PipelineRun con estos parámetros
6. El Pipeline se ejecuta automáticamente, clonando el código, construyendo la imagen con la etiqueta del hash del commit, y desplegando la aplicación

Esta integración entre GitHub y Tekton representa la verdadera esencia de la integración y entrega continuas (CI/CD). Al eliminar los pasos manuales entre el desarrollo y el despliegue, aceleramos el ciclo de feedback y reducimos la posibilidad de errores humanos.

Además, al utilizar el hash del commit como etiqueta de la imagen, creamos una trazabilidad directa entre cada versión de la aplicación desplegada y el código exacto que la generó, lo que es invaluable para la depuración y el cumplimiento de auditorías.

En un entorno empresarial, este tipo de automatización permite que los equipos de desarrollo se concentren en crear valor para los usuarios finales, en lugar de preocuparse por los procesos de construcción y despliegue. Con cada push a main, los cambios fluyen automáticamente hacia el entorno de producción, siguiendo el principio de "push with confidence" que caracteriza a las organizaciones de alto rendimiento.

> 🚀 "Si decides hacer solo las cosas que sabes que van a funcionar, dejarás un montón de oportunidades encima de la mesa". Jeff Bezos.
