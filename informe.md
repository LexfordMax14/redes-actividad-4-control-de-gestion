# Informe: control de congestión

## Parte 2: preguntas previas

### 1. ¿Por qué sirve Stop & Wait como base para Go-Back-N? ¿Qué similitud tienen?

Ambos usan números de secuencia, ACKs (acuses de recibo) y timeouts para detectar pérdidas y retransmitir datos. Por eso se puede reutilizar como base el manejo de segmentos, confirmaciones y retransmisiones de Stop & Wait. Stop & Wait mantiene un solo segmento pendiente de confirmación; Go-Back-N permite varios mediante una ventana de envío y usa ACKs acumulativos. Ante un timeout, Go-Back-N retransmite desde el segmento pendiente más antiguo.

### 2. ¿Cambia recv al usar SocketUDP y SlidingWindowCC en Stop & Wait?

La lógica de recepción de Stop & Wait se mantiene: recibir el segmento esperado, entregar sus datos una sola vez y enviar el ACK correspondiente, confirmando también los duplicados sin volver a entregar sus datos. SlidingWindowCC organiza la ventana del emisor y SocketUDP facilita el manejo de timers; su uso no exige por sí solo cambiar esa lógica del receptor. Pueden necesitarse ajustes en las llamadas al socket y en el manejo de timers al integrar SocketUDP.

## Parte 3: ventana inicial de congestión

Con el control de congestión activado, `window_size` inicialmente vale **1 segmento**, porque `CongestionControl` comienza en slow start con `cwnd = 1 MSS`. Como `MSS = 8 bytes`, la cantidad de segmentos completos que caben en la ventana es `cwnd / MSS = 8 / 8 = 1`. El modo debug confirmó este valor. Con el control desactivado, se mantiene la ventana fija de 8 segmentos.

## Pruebas finales

Se utilizó un cliente y un servidor simples en localhost mediante `send` y `recv` con `mode="go_back_n"`. Los archivos binarios se leyeron y escribieron en una carpeta temporal y se compararon byte por byte; se recibieron en bloques de hasta 127 bytes. Todos los archivos llegaron íntegros y las conexiones se cerraron correctamente.

### Evolución de la ventana

Sin pérdida inducida, el archivo de 2048 B tardó 0,395 s, con 257 segmentos de datos (incluyendo el segmento de longitud) y 257 ACKs. No se observaron timeouts espontáneos en esa ejecución. La ventana comenzó en 1 segmento; `cwnd` creció con los ACKs y se mantuvo en slow start con `ssthresh = None`.

Con pérdidas se observaron timeouts: `ssthresh` pasó a la mitad de la `cwnd` anterior, `cwnd` volvió a 8 bytes y la ventana a 1 segmento. Al alcanzar el umbral se pasó a congestion avoidance. Las pruebas comprobaron los valores y cambios de estado después de cada evento. El debug registra `cwnd`, `window_size`, estado y `ssthresh`.

### Comparación con 20% de pérdida

El enunciado menciona tanto 100 B como más de 1000 B, por lo que se probaron 100 B y 2048 B, cinco veces por modo. Se configuró un timeout de 0,5 s y una probabilidad de pérdida del 20% por envío de datos y ACKs, usando semillas reproducibles. Esta es una probabilidad, no una proporción exacta de descartes en cada ejecución. No se indujeron pérdidas durante el handshake ni el cierre.

El tiempo corresponde a la ejecución de `send`, incluyendo retransmisiones y debug, pero excluyendo conexión y cierre. Los mensajes contados son intentos de envío de segmentos de datos y ACKs, incluyendo retransmisiones y envíos descartados; no incluyen handshake ni cierre. Ambos modos usaron bloques de datos de 8 bytes. Sin control, la ventana permaneció fija en 8 segmentos.

| Archivo | Control de congestión | Tiempo promedio (s) | Mensajes promedio |
|---|---|---:|---:|
| 100 B | Sí | 2.659 | 43.8 |
| 100 B | No | 2.042 | 60.4 |
| 2048 B | Sí | 42.954 | 802.0 |
| 2048 B | No | 32.505 | 1372.0 |

Para el archivo de más de 1000 B, Go-Back-N sin control fue más rápido en promedio, pero intercambió más mensajes. Con control, la reducción de ventana después de los timeouts limitó las retransmisiones, a costa de un mayor tiempo de envío. Para 100 B también fue más rápido sin control en promedio, aunque hubo variación entre repeticiones. Estos resultados corresponden a esta implementación en localhost, sin congestión real ni retardo artificial, y no establecen qué modo será más rápido en cualquier red.

Las pruebas revelaron un caso de bloqueo cuando se perdía el último ACK y la ventana se reducía: al esperar el cierre, el receptor no confirmaba duplicados anteriores al último segmento recibido. Se corrigió para repetir el último ACK acumulativo ante esos duplicados y se añadió una prueba de regresión.

Evidencia: `resultados_pruebas.csv` contiene las 21 ejecuciones y `debug_pruebas.txt` registra la evolución de las ventanas y las pérdidas inducidas. Para repetir las pruebas: `python -B pruebas.py`. Las pérdidas se simulan dentro del programa; no se modificó la configuración de red del computador.
