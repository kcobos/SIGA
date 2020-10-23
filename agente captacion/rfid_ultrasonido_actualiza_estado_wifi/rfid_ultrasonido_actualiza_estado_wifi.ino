#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

/* WIFI */
const char* ssid      = "";  // WIFI SSID
const char* password  = "";  // WIFI pass
/* END OF WIFI */

/* SERVER */
const char* host      = "192.168.1.x"; // IP del servidor
const int   port      = 8080;          // Puerto
/* END OF SERVER */

/* PLAZA*/
const unsigned int id = 1; // ID de plaza
int estado = 0;
/* END OF PLAZA*/

/* RFID */
#define RST_PIN  D3 // RST-PIN for RC522 - RFID
#define SS_PIN   D8 // SDA-PIN for RC522 - RFID 
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance
String uid = "";
/* END OF RFID */

/* ULTRASONIDO */
#define pin_trig D1
#define pin_echo D2
/* END OF ULTRASONIDO */

/* DEBUGGING */
//#define SERIAL
// quitar LEDS
/* END OF DEBUGGING */

/* LEDS */
#define LEDS
#ifdef LEDS
#define pin_led_rojo 1
#define pin_led_verde 3
#endif
unsigned long tiempo = 0;
bool blink_verde = false;
/* END OF LEDS */

#define dist_min 40 // distancia minima plaza ocupada 40cm
bool comprobando = false;

bool ocupado = false;
bool acreditado = false;
bool envia_datos = true;
bool fallo_conexion = false;
bool enviar_datos_fallo = false;

/* TRIGGER para leer distancia cada 5 segundos */
bool leer_distancia = false;
void timer0_ISR (void) {
  leer_distancia = true;
  timer0_write(ESP.getCycleCount() + 80000000L * 5); // 80MHz == 1seg

  enviar_datos_fallo = fallo_conexion;
  fallo_conexion = false;
}
/* END OF TRIGGER */

void setup() {
#ifdef SERIAL
  Serial.begin(115200);

  /* CONECTAR WIFI */
  Serial.print("Conectando a: ");
  Serial.println(ssid);
#endif
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
#ifdef SERIAL
    Serial.print(".");
#endif
  }
#ifdef SERIAL
  Serial.println("");
  Serial.println("Conectado");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("\n");
#endif
  /* END OF CONECTAR WIFI */

  /* SETUP RFID */
  SPI.begin();           // Init SPI bus
  mfrc522.PCD_Init();    // Init MFRC522
  /* END OF SETUP RFID */

  /* SETUP ULTRASONIDOS */
  pinMode(pin_trig, OUTPUT);
  pinMode(pin_echo, INPUT);
  /* END OF SETUP ULTRASONIDOS */

  /* TRIGGER */
  noInterrupts();
  timer0_isr_init();
  timer0_attachInterrupt(timer0_ISR);
  timer0_write(ESP.getCycleCount() + 80000000L); // 80MHz == 1sec
  interrupts();
  /* END 0F TRIGGER */

  /* LEDS */
#ifdef LEDS
  pinMode(pin_led_rojo, FUNCTION_3);
  pinMode(pin_led_verde, FUNCTION_3);
  pinMode(pin_led_rojo, OUTPUT);
  pinMode(pin_led_verde, OUTPUT);
#endif
  /* END OF LEDS */
}

void loop() {
  /* LEDS */
  if (fallo_conexion || envia_datos || enviar_datos_fallo) {
#ifdef SERIAL
    //      Serial.println("leds");
#endif
    if (tiempo + 500 < millis()) {
#ifdef SERIAL
      Serial.println("blink");
#endif
      if (blink_verde) {
#ifdef LEDS
        digitalWrite(pin_led_rojo, HIGH);
        digitalWrite(pin_led_verde, LOW);
#endif
      } else {
#ifdef LEDS
        digitalWrite(pin_led_verde, HIGH);
        digitalWrite(pin_led_rojo, LOW);
#endif
      }
      blink_verde = !blink_verde;
      tiempo = millis();
    }
  } else if (ocupado && !acreditado) {
#ifdef LEDS
    digitalWrite(pin_led_rojo, HIGH);
    digitalWrite(pin_led_verde, LOW);
#endif
  } else if (ocupado && acreditado) {
#ifdef LEDS
    digitalWrite(pin_led_verde, HIGH);
    digitalWrite(pin_led_rojo, LOW);
#endif
  } else if (!ocupado) {
#ifdef LEDS
    digitalWrite(pin_led_rojo, LOW);
    digitalWrite(pin_led_verde, LOW);
#endif
  }
  /* END OF LEDS */
  /* MEDIR DISTANCIA */
  if (leer_distancia) {
    digitalWrite(pin_trig, LOW);
    delayMicroseconds(4);
    digitalWrite(pin_trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(pin_trig, LOW);

    long duracion = pulseIn(pin_echo, HIGH);
    double distancia = duracion * 10 / 292 / 2.0;
#ifdef SERIAL
    Serial.println(distancia);
#endif

    if (distancia < dist_min && !ocupado) {
      ocupado = true;
      envia_datos = true;
      estado = 2;
    } else if (distancia > dist_min && ocupado) {
      ocupado = false;
      acreditado = false;
      envia_datos = true;
      estado = 0;
    }

    leer_distancia = false;
  }
  /* END OF MEDIR DISTANCIA */

  /* LEER TARJETA */
  if (ocupado && !acreditado) {
#ifdef SERIAL
    Serial.println("ocupado y no acreditado");
#endif
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      if (!comprobando == !fallo_conexion) {
        comprobando = true;
#ifdef SERIAL
        Serial.println("leyendo tarjeta");
#endif
        uid = byte_array_to_string(mfrc522.uid.uidByte, mfrc522.uid.size);
#ifdef SERIAL
        Serial.println("tarjeta leida");
        Serial.println(uid);
#endif
#ifdef LEDS
        digitalWrite(pin_led_verde, HIGH);
        digitalWrite(pin_led_rojo, HIGH);
#endif
        int ccacreditacion = compruebaAcreditacion(uid);
        if (ccacreditacion == 0) {
          acreditado = true;
          envia_datos = true;
          estado = 1;
          fallo_conexion = false;
          uid = "";
        } else if (ccacreditacion == 1) {
          fallo_conexion = false;
          uid = "";
        } else if (ccacreditacion == -1) {
          fallo_conexion = true;
        }
        comprobando = false;
      }
    }
  }
  /* END OF LEER TARJETA */

  /* ENVIA DATOS */
  if (envia_datos && !fallo_conexion)
    if (actualizarEstado(estado)) {
      envia_datos = false;
      fallo_conexion = false;
    } else {
      envia_datos = true;
      fallo_conexion = true;
    }
  /* END OF ENVIA DATOS */

  /* FALLO DE CONEXION */
  if (enviar_datos_fallo && !fallo_conexion) {
    if (ocupado && uid != "") {
      if (!comprobando) {
        comprobando = true;
        int ccacreditacion = compruebaAcreditacion(uid);
        if (ccacreditacion == 0) {
          acreditado = true;
          envia_datos = true;
          estado = 1;
          fallo_conexion = false;
          uid = "";
        } else if (ccacreditacion == 1) {
          fallo_conexion = false;
          uid = "";
        } else if (ccacreditacion == -1) {
          fallo_conexion = true;
        }
        comprobando = false;
      }
    }
    if (envia_datos) {
      if (actualizarEstado(estado)) {
        envia_datos = false;
        fallo_conexion = false;
      }
    }
    enviar_datos_fallo = false;
  }
  /* END OF FALLO CONEXION */
}


String byte_array_to_string(byte *buffer, byte bufferSize) {
  String str = "";
  for (byte i = 0; i < bufferSize; i++) {
    str = str + String(buffer[i] < 0x10 ? " 0" : " ");
    str = str + String(buffer[i], HEX);
  }
  str.trim();
  str.replace(" ", "%20");
  return str;
}

/*
   Comprueba uid llamando al servidor
*/
int compruebaAcreditacion(String uid) {
#ifdef SERIAL
  Serial.println("comprueba acreditacion");
#endif
  WiFiClient client;
  if (!client.connect(host, port)) {
#ifdef SERIAL
    Serial.println("Fallo conexion acreditacion");
#endif
    return -1;
  }
  String url = "/acreditacion/" + uid;

  client.print("GET " + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 2000) {
#ifdef SERIAL
      Serial.println(">>> Client Timeout acreditacion");
#endif
      client.stop();
      return -1;
    }
  }

  while (client.available()) {
    String res = client.readStringUntil('\n');
  }

  int r = 1;
  String res = client.readStringUntil('\r');
  client.stop();
  StaticJsonBuffer<40> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(res);
  if (root.success() && root["existe"]) {
    r = 0;
  }
#ifdef SERIAL
  Serial.println(r);
#endif
  return r;
}

/*
   Envia por wifi el estado tomado como parametro
*/
bool actualizarEstado(int _estado) {
#ifdef SERIAL
  Serial.println("actualizar estado");
#endif
  WiFiClient client;
  if (!client.connect(host, port)) {
#ifdef SERIAL
    Serial.println("Fallo conexion actualizar");
#endif
    return false;
  }

  String url = "/plaza/" + String(id) + "/estado/" + String(_estado);

  String peticion = "PUT " + url + " HTTP/1.1\r\n" +
                    "Host: " + host + "\r\n" +
                    "Connection: close\r\n" +
                    "Content-Length: 0\r\n\r\n";

#ifdef SERIAL
  Serial.println(peticion);
#endif
  client.print(peticion);

  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 2000) {
#ifdef SERIAL
      Serial.println(">>> Client Timeout actualizar");
#endif
      client.stop();
      return false;
    }
  }

#ifdef SERIAL
  Serial.println("\n");
#endif
  return true;
}
