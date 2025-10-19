# Guía de Debugging - Clinic Management System

Esta guía te ayudará a configurar y usar el debugger de VSCode para todos los microservicios del proyecto.

## Requisitos Previos

1. **VSCode** instalado con las siguientes extensiones:
   - Python (ms-python.python)
   - Pylance (ms-python.vscode-pylance)
   - Python Debugger (ms-python.debugpy)

2. **Docker Desktop** corriendo (para PostgreSQL y RabbitMQ)

## Configuración Inicial

### 1. Abrir el proyecto en VSCode

```bash
cd "h:\Especializacion\Construcción de software\Clinic-Management-System"
code .
```

### 2. Instalar dependencias de Python

Para Identity Service:
```bash
cd identity-service
pip install -r requirements.txt
pip install debugpy  # Si no está instalado
```

### 3. Iniciar la infraestructura (PostgreSQL y RabbitMQ)

```bash
# Desde la raíz del proyecto
docker-compose up -d postgres rabbitmq
```

O usa la tarea de VSCode:
- Presiona `Ctrl+Shift+P`
- Escribe "Tasks: Run Task"
- Selecciona "Start All Infrastructure"

## Cómo Debuggear

### Opción 1: Debuggear un servicio específico

1. **Marcar Breakpoints**:
   - Abre el archivo que quieres debuggear (ejemplo: `identity-service/src/main.py`)
   - Haz clic en el margen izquierdo (junto al número de línea)
   - Aparecerá un punto rojo indicando el breakpoint

2. **Iniciar el Debugger**:
   - Presiona `F5` o ve a la pestaña "Run and Debug" (`Ctrl+Shift+D`)
   - Selecciona la configuración apropiada:
     - **Identity Service - FastAPI**: Para debuggear el servicio completo
     - **Identity Service - Main.py**: Para debuggear desde main.py
     - **Patient Service - FastAPI**: Para debuggear patient service
     - etc.
   - Click en el botón de play verde (▶️)

3. **Interactuar con el servicio**:
   - El servidor se inicia en modo debug
   - Abre tu navegador en `http://localhost:8001/docs` (o el puerto del servicio)
   - Cuando el código llegue a un breakpoint, la ejecución se pausará
   - Podrás inspeccionar variables en el panel izquierdo

### Opción 2: Debuggear todos los servicios a la vez

1. En el menú de debug, selecciona **"All Services"**
2. Esto iniciará todos los microservicios en modo debug simultáneamente
3. Puedes marcar breakpoints en cualquiera de los servicios

### Opción 3: Debuggear el archivo actual

1. Abre cualquier archivo Python
2. Presiona `F5`
3. Selecciona **"Python: Current File"**
4. El archivo se ejecutará en modo debug

## Controles del Debugger

| Tecla | Acción | Descripción |
|-------|--------|-------------|
| `F5` | Continue | Continuar hasta el siguiente breakpoint |
| `F10` | Step Over | Ejecutar la línea actual y pasar a la siguiente |
| `F11` | Step Into | Entrar dentro de la función que se está llamando |
| `Shift+F11` | Step Out | Salir de la función actual |
| `Ctrl+Shift+F5` | Restart | Reiniciar el debugger |
| `Shift+F5` | Stop | Detener el debugger |

## Panel de Debug

Cuando el debugger está activo, verás varios paneles:

### 1. Variables
- Muestra todas las variables locales y globales
- Puedes expandir objetos para ver sus propiedades
- Puedes modificar valores en tiempo real

### 2. Watch
- Agrega expresiones para monitorear
- Ejemplo: `user.email`, `len(items)`, etc.

### 3. Call Stack
- Muestra la pila de llamadas actual
- Útil para ver cómo llegaste al breakpoint actual

### 4. Breakpoints
- Lista todos los breakpoints activos
- Puedes habilitarlos/deshabilitarlos temporalmente

### 5. Debug Console
- Ejecuta código Python en el contexto actual
- Ejemplo: `print(variable)`, `type(obj)`, etc.

## Ejemplos Prácticos

### Debuggear el endpoint de Login

1. Abre `identity-service/src/application/use_cases/login_user.py`
2. Marca un breakpoint en la línea del método `execute()`
3. Inicia el debugger con "Identity Service - FastAPI"
4. En el navegador, ve a `http://localhost:8001/docs`
5. Ejecuta el endpoint POST `/api/v1/login`
6. El código se detendrá en tu breakpoint

### Debuggear la creación de usuarios

1. Abre `identity-service/src/application/use_cases/create_user.py`
2. Marca breakpoint en el método `execute()`
3. Inicia debugger
4. Llama al endpoint POST `/api/v1/register` desde Swagger UI
5. Inspecciona el objeto `request` para ver los datos recibidos

### Debuggear validación de tokens

1. Abre `identity-service/src/infrastructure/security/jwt_handler.py`
2. Marca breakpoint en `verify_token()`
3. Haz una petición con autenticación
4. Inspecciona el token y el payload

## Debugging con breakpoint() en código

Si prefieres usar breakpoints en el código directamente:

```python
# En cualquier parte del código
def my_function(data):
    breakpoint()  # El debugger se detendrá aquí
    # ... resto del código
```

Cuando uses `breakpoint()`, se abrirá el debugger de Python (pdb) en la terminal.

Comandos de pdb:
- `n` - siguiente línea
- `s` - entrar en función
- `c` - continuar
- `l` - mostrar código
- `p variable` - imprimir variable
- `q` - salir

## Tareas Útiles de VSCode

Presiona `Ctrl+Shift+P` y escribe "Tasks: Run Task" para acceder a:

- **Install Identity Service Dependencies**: Instala dependencias
- **Start PostgreSQL**: Inicia solo PostgreSQL
- **Start RabbitMQ**: Inicia solo RabbitMQ
- **Start All Infrastructure**: Inicia PostgreSQL y RabbitMQ
- **Stop All Docker Services**: Detiene todos los contenedores
- **Run Identity Service Tests**: Ejecuta tests del servicio

## Solución de Problemas

### El debugger no se conecta

1. Verifica que `debugpy` esté instalado: `pip install debugpy`
2. Verifica que el puerto no esté en uso
3. Reinicia VSCode

### Los breakpoints aparecen en gris (no se activan)

1. Verifica que el archivo esté guardado
2. Verifica que `justMyCode` esté en `false` en launch.json
3. Reinicia el debugger

### Variables no se muestran

1. Asegúrate de que el breakpoint se haya alcanzado
2. Verifica que estés en el contexto correcto de la función
3. Usa el Debug Console para ejecutar comandos manualmente

### Error "Module not found"

1. Verifica que `PYTHONPATH` esté configurado correctamente en launch.json
2. Verifica que estés en el directorio correcto (`cwd`)
3. Reinstala las dependencias

## Recursos Adicionales

- [Documentación oficial de VSCode Python Debugging](https://code.visualstudio.com/docs/python/debugging)
- [Documentación de debugpy](https://github.com/microsoft/debugpy)
- [FastAPI Debugging Guide](https://fastapi.tiangolo.com/tutorial/debugging/)

## Configuración Avanzada

### Debug con variables de entorno personalizadas

Edita `.vscode/launch.json` y agrega al objeto `env`:

```json
"env": {
    "PYTHONPATH": "${workspaceFolder}/identity-service/src",
    "DEBUG": "True",
    "LOG_LEVEL": "DEBUG"
}
```

### Debug con argumentos personalizados

Modifica el array `args` en la configuración:

```json
"args": [
    "main:app",
    "--reload",
    "--host", "127.0.0.1",
    "--port", "8001",
    "--log-level", "debug"
]
```

### Conditional Breakpoints

1. Haz clic derecho en un breakpoint existente
2. Selecciona "Edit Breakpoint"
3. Agrega una condición (ejemplo: `user.id == 123`)
4. El breakpoint solo se activará cuando la condición sea verdadera

### Logpoints

1. Haz clic derecho en el margen izquierdo
2. Selecciona "Add Logpoint"
3. Escribe el mensaje (ejemplo: `User: {user.email}`)
4. El mensaje se imprimirá sin pausar la ejecución
