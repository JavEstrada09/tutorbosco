"""Catálogo local: claves estables para los casos de retroalimentación de S-009."""

DEMO_EXERCISES = {
    "PROG-COM": {
        "Git y GitHub avanzado": ("git-merge-v1", "Usted trabaja en una rama de funcionalidad. Explique cómo integraría main conservando el historial y cómo resolvería un conflicto antes de publicar sus cambios."),
        "Código limpio y refactoring": ("refactoring-v1", "Una función calcula un total, imprime el resultado y guarda un archivo. Proponga cómo separaría usted esas responsabilidades sin cambiar el resultado."),
        "Sistemas de información y bases de datos": ("sistemas-bd-v1", "Usted diseña un registro de ventas. Identifique las entidades Cliente, Venta y Producto, sus claves y cómo relacionaría una venta con varios productos."),
        "Ingeniería de prompts": ("prompts-v1", "Redacte usted un prompt para explicar una nota de venta a un principiante. Incluya objetivo, contexto, restricciones y formato esperado."),
        "El LLM por dentro y su API": ("llm-api-v1", "Explique usted qué debe hacer un backend cuando una API de IA devuelve cuota agotada y por qué no debe exponer la clave en el navegador."),
        "Agentes de programación y desarrollo guiado por especificaciones": ("specs-v1", "Antes de pedir código a un agente, escriba usted un criterio Dado/Cuando/Entonces para impedir que un estudiante consulte las notas de otra persona."),
    },
    "BD-APL": {
        "Modelo relacional": ("relacional-v1", "Usted administra clientes y pedidos. Proponga una clave primaria para cada tabla y una clave foránea que relacione un pedido con su cliente."),
        "Consultas SQL": ("sql-v1", "Dada la tabla Venta(id, total), escriba usted una consulta que seleccione las ventas con total mayor que 100, ordenadas de mayor a menor."),
        "Normalización": ("normalizacion-v1", "Una tabla repite el nombre y teléfono del cliente en cada venta. Explique usted cómo separaría esos datos para evitar inconsistencias."),
        "Transacciones": ("transacciones-v1", "Usted transfiere Q50 entre dos cuentas. Explique qué operaciones deben ser atómicas y qué debe ocurrir si falla el segundo paso."),
        "Índices y rendimiento": ("indices-v1", "Una aplicación busca clientes por correo. Explique usted qué índice propondría y qué costo tendría al insertar nuevos registros."),
        "Copias de seguridad y recuperación": ("backup-v1", "Proponga usted un procedimiento para respaldar una base de datos y comprobar que la copia puede restaurarse sin perder los datos originales."),
    },
    "DES-WEB": {
        "HTML semántico": ("html-v1", "Escriba usted una estructura HTML semántica con encabezado, navegación y contenido principal para una página de cursos."),
        "CSS y diseño adaptable": ("css-v1", "Explique usted cómo organizaría dos columnas en escritorio y una sola en pantallas pequeñas utilizando CSS adaptable."),
        "JavaScript básico": ("js-v1", "Escriba usted una función JavaScript que reciba un precio y una cantidad, y devuelva el total sin modificar la página."),
        "Formularios y validación": ("formularios-v1", "Usted recibe una nota mediante un formulario. Describa cómo validaría que sea un entero de 0 a 100 tanto en la interfaz como en el servidor."),
        "Accesibilidad web": ("accesibilidad-v1", "Explique usted cómo asociaría una etiqueta a un campo y cómo comunicaría un error a una persona que utiliza lector de pantalla."),
        "Despliegue local": ("despliegue-v1", "Describa usted los pasos para ejecutar una aplicación Django en localhost usando un entorno virtual y configuración local."),
    },
    "REDES": {
        "Modelo OSI": ("osi-v1", "Compare usted las funciones de las capas de red y transporte e indique un ejemplo de protocolo de cada una."),
        "Direccionamiento IP": ("ip-v1", "Explique usted por qué dos equipos de una misma red necesitan direcciones IP diferentes y para qué utilizan la puerta de enlace."),
        "Subredes": ("subredes-v1", "Para la red 192.168.1.0/26, determine usted la dirección de difusión y el intervalo de direcciones utilizables."),
        "Protocolos de transporte": ("transporte-v1", "Compare usted TCP y UDP e indique cuál elegiría para transferir un archivo que no puede perder datos, justificando su decisión."),
        "Seguridad básica de red": ("seguridad-red-v1", "Proponga usted dos medidas para proteger una red local y explique qué amenaza reduce cada una."),
        "Diagnóstico de conectividad": ("conectividad-v1", "Un equipo llega a una dirección IP pero no resuelve nombres. Explique usted qué comprobaría para diagnosticar el problema de DNS."),
    },
}
