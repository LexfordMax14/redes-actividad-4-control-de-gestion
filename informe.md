# Informe: control de congestión

## Parte 2: preguntas previas

### 1. ¿Por qué sirve Stop & Wait como base para Go-Back-N? ¿Qué similitud tienen?

Ambos usan números de secuencia, ACKs (acuses de recibo) y timeouts para detectar pérdidas y retransmitir datos. Por eso se puede reutilizar como base el manejo de segmentos, confirmaciones y retransmisiones de Stop & Wait. Stop & Wait mantiene un solo segmento pendiente de confirmación; Go-Back-N permite varios mediante una ventana de envío y usa ACKs acumulativos. Ante un timeout, Go-Back-N retransmite desde el segmento pendiente más antiguo.

### 2. ¿Cambia recv al usar SocketUDP y SlidingWindowCC en Stop & Wait?

La lógica de recepción de Stop & Wait se mantiene: recibir el segmento esperado, entregar sus datos una sola vez y enviar el ACK correspondiente, confirmando también los duplicados sin volver a entregar sus datos. SlidingWindowCC organiza la ventana del emisor y SocketUDP facilita el manejo de timers; su uso no exige por sí solo cambiar esa lógica del receptor. Pueden necesitarse ajustes en las llamadas al socket y en el manejo de timers al integrar SocketUDP.
