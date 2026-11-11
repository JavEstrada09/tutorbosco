"""Casos explícitos: no se evalúa texto libre mediante coincidencias parciales."""

from dataclasses import dataclass

from tutor.demo_exercises import DEMO_EXERCISES


@dataclass(frozen=True)
class DemoFeedbackCase:
    correct: str
    incorrect: str
    success: str
    correction: str
    brief: str
    detailed: str


DEMO_FEEDBACK = {
    "git-merge-v1": DemoFeedbackCase(
        "Integro main en mi rama con git merge, resuelvo los conflictos, ejecuto las pruebas y después publico los cambios.",
        "Sobrescribo main y elimino el historial para evitar los conflictos.",
        "Usted conserva el historial e incluye resolución de conflictos y pruebas antes de publicar.",
        "Sobrescribir main y eliminar el historial puede perder trabajo; no resuelve correctamente los conflictos.",
        "Revise el diff final y confirme que las pruebas pasan antes de publicar la integración.",
        "Avance paso a paso: actualice main, vuelva a su rama y ejecute git merge main. Revise cada conflicto, conserve los cambios necesarios, ejecute las pruebas y confirme la integración antes de publicar.",
    ),
    "refactoring-v1": DemoFeedbackCase(
        "Separo el cálculo del total, la presentación y el guardado en funciones independientes y conservo pruebas del resultado.",
        "Agrego más responsabilidades a la misma función y cambio el total sin comprobarlo.",
        "Usted separa responsabilidades y protege el comportamiento mediante pruebas.",
        "Agregar responsabilidades y cambiar el total sin comprobarlo dificulta el mantenimiento y altera el comportamiento.",
        "Compare los totales antes y después del refactoring mediante las mismas entradas.",
        "Primero escriba un caso con precio y cantidad conocidos. Extraiga el cálculo a una función que devuelva el total; después separe la impresión y el archivo. Ejecute el mismo caso tras cada extracción.",
    ),
    "sistemas-bd-v1": DemoFeedbackCase(
        "Defino Cliente, Venta y Producto con sus claves, y DetalleVenta relaciona cada venta con sus productos y cantidades.",
        "Guardo todos los productos en una sola celda de Venta sin claves ni relaciones.",
        "Usted identifica las entidades y resuelve la relación entre ventas y productos mediante el detalle.",
        "Una celda con varios productos impide representar y validar correctamente las relaciones.",
        "Añada claves foráneas y compruebe una venta con dos productos en DetalleVenta.",
        "Dibuje Cliente y Venta unidos por cliente_id. Cree Producto con su clave. Luego escriba dos filas de DetalleVenta con la misma venta_id, diferentes producto_id y sus cantidades.",
    ),
    "prompts-v1": DemoFeedbackCase(
        "Objetivo: explique una nota de venta. Contexto: estudiante principiante. Restricción: no invente datos. Formato: definición y ejemplo breve.",
        "Haga cualquier cosa con ventas, invente los datos y responda sin formato.",
        "Usted incluye objetivo, contexto, restricción y formato para orientar la explicación.",
        "La respuesta permite inventar datos y no fija un objetivo ni un formato verificables.",
        "Pruebe el prompt y revise si la salida contiene la definición y el ejemplo solicitados.",
        "Construya cuatro líneas: qué debe explicar, para quién, qué no puede inventar y cómo debe presentar la salida. Después compare una respuesta con cada una de esas cuatro condiciones.",
    ),
    "llm-api-v1": DemoFeedbackCase(
        "El backend informa la cuota agotada, ofrece modo demo y conserva la clave fuera del navegador.",
        "Publico la clave en JavaScript y repito llamadas sin límite cuando se agota la cuota.",
        "Usted propone un aviso seguro y una alternativa local sin exponer la clave.",
        "Publicar la clave permite uso ajeno; repetir llamadas sin límite no resuelve la cuota agotada.",
        "Compruebe que un error 429 active el aviso y que ninguna respuesta HTTP contenga la clave.",
        "Separe servidor y navegador en un diagrama. La clave permanece en el servidor. Ante 429, detenga la consulta externa, muestre el aviso y seleccione una respuesta local aplicable sin revelar detalles internos.",
    ),
    "specs-v1": DemoFeedbackCase(
        "Dado un estudiante autenticado, cuando solicita las notas de otro estudiante, entonces el servidor rechaza el acceso sin revelar datos.",
        "Oculto el botón de notas ajenas y considero que con eso el acceso está protegido.",
        "Usted define una condición, una acción y un resultado verificable en el servidor.",
        "Ocultar un botón no impide una petición directa y no constituye autorización del servidor.",
        "Añada una prueba que envíe directamente un identificador de otro estudiante.",
        "Escriba tres partes: Dado identifica la sesión; Cuando describe la petición de datos ajenos; Entonces exige rechazo sin datos. Compruebe ese resultado tanto desde la interfaz como mediante una petición directa.",
    ),
    "relacional-v1": DemoFeedbackCase(
        "Cliente tiene cliente_id como clave primaria; Pedido tiene pedido_id y cliente_id como clave foránea hacia Cliente.",
        "Uso el nombre repetido del cliente como única relación y no defino claves.",
        "Usted distingue claves primarias y la referencia del pedido a su cliente.",
        "Los nombres pueden repetirse y no sustituyen una relación mediante claves.",
        "Pruebe dos clientes con el mismo nombre y pedidos con distintos cliente_id.",
        "Cree primero Cliente con identificadores 1 y 2. Cree un Pedido con pedido_id propio y cliente_id=1. Compruebe que la clave foránea impide referenciar un cliente inexistente.",
    ),
    "sql-v1": DemoFeedbackCase(
        "SELECT id, total FROM Venta WHERE total > 100 ORDER BY total DESC;",
        "SELECT id, total FROM Venta WHERE total < 100 ORDER BY total ASC;",
        "Usted filtra totales mayores que 100 y los ordena de mayor a menor.",
        "La comparación menor que 100 y el orden ascendente contradicen lo solicitado.",
        "Compruebe la consulta con totales 80, 100, 120 y 200: deben salir 200 y 120.",
        "Separe la consulta en pasos: FROM elige Venta; WHERE total > 100 excluye 80 y 100; ORDER BY total DESC coloca primero 200 y después 120. Compare esas dos filas con el resultado obtenido.",
    ),
    "normalizacion-v1": DemoFeedbackCase(
        "Separo Cliente con nombre y teléfono, y Venta referencia al cliente mediante cliente_id.",
        "Mantengo el teléfono duplicado en cada venta y lo corrijo manualmente en algunas filas.",
        "Usted elimina la repetición del dato de cliente y conserva la relación con cada venta.",
        "Corregir solo algunas copias deja teléfonos contradictorios para el mismo cliente.",
        "Actualice una vez el teléfono de Cliente y compruebe dos ventas relacionadas.",
        "Identifique qué datos describen al cliente y cuáles a la venta. Mueva nombre y teléfono a Cliente; deje cliente_id en Venta. Cambie el teléfono una sola vez y consulte todas las ventas del cliente.",
    ),
    "transacciones-v1": DemoFeedbackCase(
        "El débito de Q50 y el crédito de Q50 forman una transacción; si falla un paso, se revierten ambos.",
        "Confirmo el débito aunque falle el crédito y dejo la transferencia incompleta.",
        "Usted trata débito y crédito como una unidad atómica con reversión ante fallos.",
        "Confirmar solo el débito produce una transferencia incompleta y pierde consistencia.",
        "Simule un fallo antes del crédito y compruebe que ambos saldos originales se conservan.",
        "Anote los dos saldos iniciales. Abra una transacción, reste Q50 y sume Q50. Confirme solo si ambos pasos funcionan; ante el fallo de cualquiera, revierta y compare los saldos con los iniciales.",
    ),
    "indices-v1": DemoFeedbackCase(
        "Creo un índice sobre correo para acelerar la búsqueda y considero el costo de mantenerlo en cada inserción.",
        "Creo índices en todas las columnas porque nunca afectan las inserciones.",
        "Usted relaciona el índice con el filtro de correo y reconoce el costo de escritura.",
        "Cada índice consume espacio y necesita mantenimiento; no conviene agregarlos sin medir.",
        "Compare el plan de la búsqueda por correo antes y después de crear el índice.",
        "Escriba la consulta que filtra por correo. Revise su plan, cree un índice para esa columna y compare nuevamente. Mida también una inserción para observar el trabajo de actualizar el índice.",
    ),
    "backup-v1": DemoFeedbackCase(
        "Genero un respaldo consistente, lo restauro en una base separada y verifico los registros sin sobrescribir el original.",
        "Sobrescribo la única base con una copia que nunca probé restaurar.",
        "Usted incluye restauración comprobada y aislamiento del original.",
        "Sobrescribir la única base con una copia no verificada puede destruir los datos disponibles.",
        "Registre fecha, cantidad de filas y resultado de una consulta en la base restaurada.",
        "Conserve el original, cree la copia mediante un procedimiento consistente y restaure en otra ubicación. Compare tablas, conteos y una consulta conocida antes de considerar utilizable ese respaldo.",
    ),
    "html-v1": DemoFeedbackCase(
        "Organizo la página con header para el encabezado, nav para los enlaces y main para el contenido de cursos.",
        "Uso solamente div sin distinguir encabezado, navegación ni contenido principal.",
        "Usted asigna etiquetas semánticas a las regiones solicitadas.",
        "Usar solo contenedores genéricos no expresa la función de las regiones de la página.",
        "Compruebe que exista un contenido principal identificable y navegación con enlaces descriptivos.",
        "Dibuje tres regiones. Coloque el título en header, los enlaces en nav y los cursos en main. Revise la estructura con el teclado y confirme que cada región tiene una función reconocible.",
    ),
    "css-v1": DemoFeedbackCase(
        "Uso una cuadrícula de dos columnas y una media query que cambia a una columna en pantallas pequeñas.",
        "Fijo dos columnas de ancho grande sin adaptar el diseño al tamaño de pantalla.",
        "Usted adapta la distribución mediante una regla para pantallas pequeñas.",
        "Dos columnas rígidas pueden desbordar la pantalla y dificultar la lectura en móviles.",
        "Pruebe el diseño a 360 px y en escritorio, comprobando que no haya desplazamiento horizontal.",
        "Empiece con una columna flexible. Añada una media query para disponer dos columnas cuando haya espacio suficiente. Reduzca el ancho de la ventana y compruebe legibilidad y ausencia de desbordamiento.",
    ),
    "js-v1": DemoFeedbackCase(
        "function total(precio, cantidad) { return precio * cantidad; }",
        "function total(precio, cantidad) { document.body.innerHTML = precio + cantidad; }",
        "Usted devuelve el producto de precio y cantidad sin modificar la página.",
        "Sumar no calcula el total y escribir en document.body introduce un efecto no solicitado.",
        "Pruebe total(10, 3): el resultado debe ser 30 sin cambios en el documento.",
        "Identifique las dos entradas, multiplíquelas y devuelva el resultado con return. Compruebe 10 por 3 igual a 30 y después una cantidad cero. Mantenga la función sin acceso al DOM.",
    ),
    "formularios-v1": DemoFeedbackCase(
        "Valido un entero de 0 a 100 en la interfaz y repito la validación en el servidor antes de guardar.",
        "Valido solo con JavaScript y acepto cualquier valor que llegue al servidor.",
        "Usted mantiene la validación de servidor además de la ayuda de la interfaz.",
        "La validación del navegador puede omitirse; el servidor debe rechazar valores inválidos.",
        "Pruebe -1, 101, 59.5 y texto mediante peticiones directas y confirme que no se guardan.",
        "Primero compruebe que el valor sea un entero. Después valide el intervalo inclusivo de 0 a 100 en el servidor. Envíe valores fuera de rango sin utilizar la interfaz y compruebe que la base no cambió.",
    ),
    "accesibilidad-v1": DemoFeedbackCase(
        "Asocio label y campo mediante for e id, y relaciono el error con aria-describedby y un mensaje visible.",
        "Uso solo un placeholder y un borde rojo sin texto para comunicar el error.",
        "Usted proporciona una etiqueta y una descripción de error vinculadas al campo.",
        "El color y el placeholder por sí solos no comunican una etiqueta y un error accesibles.",
        "Recorra el formulario con teclado y confirme que etiqueta y error se anuncian junto al campo.",
        "Asigne un id al campo y úselo en el for de label. Dé un id al mensaje de error y referéncielo con aria-describedby. Compruebe la lectura del campo y del mensaje sin depender del color.",
    ),
    "despliegue-v1": DemoFeedbackCase(
        "Creo un entorno virtual, instalo los requisitos, configuro variables locales, aplico migraciones y ejecuto runserver en localhost.",
        "Publico las claves en Git y ejecuto sin entorno ni migraciones.",
        "Usted incluye dependencias aisladas, configuración y preparación de la base antes del servidor.",
        "Versionar claves expone secretos y omitir migraciones deja la base sin preparar.",
        "Ejecute check y compruebe el acceso a localhost con los secretos fuera del repositorio.",
        "Siga este orden: entorno virtual, requisitos, variables locales, migrate y check. Finalmente inicie runserver en localhost. Revise git status para confirmar que la configuración secreta no se versiona.",
    ),
    "osi-v1": DemoFeedbackCase(
        "La capa de red enruta paquetes con IP y la de transporte comunica procesos con TCP o UDP.",
        "TCP es una dirección física y la capa de red solo dibuja páginas web.",
        "Usted diferencia enrutamiento y comunicación de transporte con ejemplos pertinentes.",
        "TCP no es una dirección física y la capa de red no presenta páginas web.",
        "Relacione IP con destino de red y TCP con entrega entre aplicaciones.",
        "Siga un mensaje: IP permite llevar paquetes hacia otra red; TCP organiza la comunicación entre aplicaciones. Compare una dirección IP con un puerto para distinguir ambas responsabilidades.",
    ),
    "ip-v1": DemoFeedbackCase(
        "Cada equipo necesita una IP distinta para evitar conflictos y usa la puerta de enlace para llegar a otras redes.",
        "Asigno la misma IP a todos los equipos y la puerta de enlace solo cambia nombres de archivos.",
        "Usted distingue identificación única y salida hacia otras redes.",
        "Compartir la misma IP provoca conflictos; la puerta de enlace no administra nombres de archivos.",
        "Compare una comunicación entre vecinos de la subred con otra hacia una red externa.",
        "Dibuje dos equipos con IP diferentes y la puerta de enlace. Para un destino local, comunique los equipos directamente; para un destino externo, señale el paso por la puerta de enlace.",
    ),
    "subredes-v1": DemoFeedbackCase(
        "La difusión es 192.168.1.63 y las direcciones utilizables van de 192.168.1.1 a 192.168.1.62.",
        "La difusión es 192.168.1.255 y utilizo 192.168.1.0 como dirección de equipo.",
        "Usted calcula correctamente la difusión y excluye red y difusión del intervalo utilizable.",
        "Una subred /26 tiene bloques de 64 direcciones; .255 no es la difusión del bloque que comienza en .0.",
        "Compruebe los límites del bloque .0 a .63 y reserve el primero y el último.",
        "Calcule 32 menos 26: quedan 6 bits, equivalentes a 64 direcciones. El bloque empieza en .0 y termina en .63. Reserve .0 para red y .63 para difusión; los equipos usan .1 a .62.",
    ),
    "transporte-v1": DemoFeedbackCase(
        "Elijo TCP para transferir el archivo porque ofrece entrega ordenada y retransmisión; UDP no garantiza esa entrega.",
        "Elijo UDP porque siempre garantiza entrega ordenada sin pérdidas.",
        "Usted justifica TCP mediante fiabilidad y distingue las garantías de UDP.",
        "UDP no garantiza por sí solo entrega ordenada ni retransmisión de datos perdidos.",
        "Explique cómo la retransmisión de TCP ayuda a conservar un archivo completo.",
        "Imagine que falta un segmento del archivo. TCP detecta la necesidad de recuperarlo y organiza el flujo; UDP no añade esa garantía por sí solo. Relacione esa diferencia con la exigencia de no perder datos.",
    ),
    "seguridad-red-v1": DemoFeedbackCase(
        "Configuro un firewall para limitar accesos y uso contraseñas fuertes para reducir accesos no autorizados.",
        "Desactivo el firewall y comparto una contraseña débil con toda la red.",
        "Usted asocia controles de acceso y credenciales con amenazas concretas.",
        "Desactivar controles y compartir credenciales débiles facilita accesos no autorizados.",
        "Indique qué conexiones necesita permitir y qué accesos debe bloquear el firewall.",
        "Enumere primero los servicios necesarios. Permita solo sus conexiones en el firewall y bloquee las restantes. Después use credenciales fuertes individuales y explique qué amenaza reduce cada medida.",
    ),
    "conectividad-v1": DemoFeedbackCase(
        "Reviso el servidor DNS configurado y pruebo una consulta de nombres, porque la conectividad por IP ya funciona.",
        "Borro todos los archivos del equipo porque DNS depende de los documentos locales.",
        "Usted enfoca el diagnóstico en resolución de nombres tras comprobar el acceso por IP.",
        "Borrar documentos no diagnostica DNS y puede perder información sin resolver la conectividad.",
        "Compare una consulta al DNS configurado con otra a un servidor de diagnóstico autorizado.",
        "Separe las pruebas: confirme acceso por IP, consulte un nombre con la herramienta DNS y revise el servidor configurado. Si falla esa consulta, compruebe alcance del servidor y configuración antes de cambiar otros componentes.",
    ),
}


def demo_case(exercise):
    entry = DEMO_EXERCISES.get(exercise.course.code, {}).get(exercise.topic.name)
    if (
        exercise.mode != "demo" or entry is None
        or exercise.demo_key != entry[0] or exercise.statement != entry[1]
    ):
        return None
    return DEMO_FEEDBACK.get(exercise.demo_key)


def recorded_feedback(exercise, content, grade):
    case = demo_case(exercise)
    if case is None:
        return None
    normalized = " ".join(content.casefold().split())
    if normalized == " ".join(case.correct.casefold().split()):
        assessment = case.success
    elif normalized == " ".join(case.incorrect.casefold().split()):
        assessment = case.correction
    else:
        return None
    return {
        "assessment": assessment,
        "guidance": case.detailed if grade is None or grade < 40 else case.brief,
    }
