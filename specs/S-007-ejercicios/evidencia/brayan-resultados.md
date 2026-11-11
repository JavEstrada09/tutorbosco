# Resultados independientes de Brayan - S-007

- Verificador: Brayan Hernandez / `Brayan11Hernandez`
- Autor: Jeffersson Ramos / `ramosdeleon555`
- Issue: #11
- Commit: `a6bd399ea1f33394b526c131e6cfba94e9e71e62`
- Estado: comprobaciones automatizadas ejecutadas; recorrido visual pendiente

| Criterio | Preparacion | Resultado esperado | Resultado observado | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| CA-1 | Estudiante aislado; notas 45, 59, 60 y 85; umbral 60. | Solo notas 45 y 59 debiles con umbral 60. | Los identificadores de los temas con 45 y 59 fueron los unicos seleccionados. | `brayan-casos.py`; salida en `brayan-pruebas.txt` | Cumple automaticamente |
| CA-2 | Mismo proceso con `override_settings` en 70; notas 60, 69 y 70. | Solo notas 60 y 69 debiles con umbral 70. | El servicio informo umbral efectivo 70 y selecciono solo 60 y 69. | `brayan-casos.py`; `brayan-pruebas.txt` | Cumple automaticamente |
| CA-3 | Dos temas sin nota y dos notas bajo el umbral. | Tema sin nota excluido; tema bajo el umbral incluido. | Ambos temas sin nota quedaron fuera; los calificados bajo 60 quedaron dentro. | `brayan-casos.py`; `brayan-pruebas.txt` | Cumple automaticamente |
| CA-4 | Proveedor Gemini simulado con clave sintetica, una respuesta valida y diferencia de UUID antes/despues. | Ejercicios nuevos con enunciado, curso y tema debil permitido. | Se persistio un ejercicio nuevo `real` simulado; Brayan confirmo en Edge curso, tema, enunciado y etiqueta demo en una generacion local. | `brayan-casos.py`; `brayan-pruebas.txt`; `brayan-http.txt` | Cumple automatico y visual |
| CA-5 | Caso con notas 60/85 y caso sin notas; ambos proveedores instrumentados. | Avisos distintos y proveedores no invocados. | Brayan confirmo ambos avisos y ausencia del boton; la instrumentacion comprobo llamadas demo=0 y real=0. | `brayan-casos.py`; `brayan-pruebas.txt`; `brayan-http.txt` | Cumple automatico y visual |
| CA-6 | Primera practica con tema 45; luego notas 60 y 40 antes de una practica nueva. | Las notas vigentes cambian solo la seleccion nueva. | Brayan confirmo el cambio de tema en la practica nueva y la permanencia del ejercicio/UUID historico. | `brayan-casos.py`; `brayan-pruebas.txt`; `brayan-http.txt` | Cumple automatico y visual |
| CA-7 | Anonimo, docente, curso ajeno, campo propietario, POST sin CSRF, UUID ajeno y proveedor instrumentado. | Solicitudes no autorizadas rechazadas sin generar ni revelar datos. | HTTP 302 para anonimo; 403 para los demas rechazos; Brayan confirmo el 403 docente sin datos; contexto aislado. | `brayan-casos.py`; `brayan-pruebas.txt`; `brayan-http.txt` | Cumple automatico y visual |
| CA-8 | Dos perfiles con temas debiles distintos; modo demo, clave vacia y constructor Gemini instrumentado. | Demo por perfil sin Gemini, red ni recursos externos. | Cliente Gemini=0, HTML sin URL externa y Brayan confirmo ejercicios distintos segun perfil. | `brayan-casos.py`; `brayan-pruebas.txt`; `brayan-http.txt` | Cumple automatico y visual |
| CA-9 | Conexion y 429 simulados; vacio, tema ajeno, falta de enunciado y catalogo ausente. | Fallos simulados usan alternativa segura; salidas invalidas se rechazan. | Conexion y cuota usaron demo con aviso; invalidos no persistieron; catalogo ausente no sustituyo temas. | `brayan-casos.py`; `brayan-pruebas.txt` | Cumple automaticamente |
| CA-10 | Ejercicio demo, consulta por UUID, texto HTML sintetico y notas comparadas antes/despues. | Espanol formal, UUID y relaciones estables, escape y notas intactas. | Brayan confirmo espanol, trato formal y UUID; automaticamente se comprobaron relaciones, escape y notas identicas. | `brayan-casos.py`; `brayan-pruebas.txt`; `brayan-http.txt` | Cumple automatico y visual |

## Impedimento detectado

La suite entregada no pasa en el commit probado: tanto
`tutor.test_exercises` como la suite completa terminan con 2 fallos y 14
errores. Los casos que intentan simular modo real permanecen bajo el override
demo de la clase y varios tampoco proporcionan la clave sintetica que exige
el constructor antes del metodo parcheado. Jeffersson debe corregir las
pruebas y entregar un nuevo commit; despues se repetiran las suites afectadas.

No se atribuye revision ni aprobacion a Brayan hasta que confirme los
resultados y pendientes despues de ejecutar cada criterio.
