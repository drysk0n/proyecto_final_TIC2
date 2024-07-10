#include <DHT.h> // Definimos el pin digital donde se conecta el sensor
#include <string.h>

#define DHTPIN 3 // Dependiendo del tipo de sensor

#define DHTTYPE DHT11 // Inicializamos el sensor DHT11 

DHT dht(DHTPIN, DHTTYPE);
// Definir
int relay = 2;
unsigned long tRegado;
unsigned long tData;

bool regadoAuto;
char MenReci[5];

void setup() {
  // Configuración
  pinMode(relay, OUTPUT); // Configurar relay como salida o OUTPUT
  Serial.begin(9600); // Abrir el puerto serie a la velocidad de 9600bps para trasnmicion de datos.
  tRegado = millis();
  tData = millis();
  dht.begin();
  regadoAuto = true;
}

void loop() {
  // Código principal donde ocurren en loop
  unsigned long tBucle = millis(); //Registra el tiempo al empezar cada bucle:


    if (Serial.available() >= 4) {  // Se asegura de recibir 4 caracteres
        char buffer[5];  
        Serial.readBytes(buffer, 4);  
        buffer[4] = '\0';  
        Serial.println(buffer);
        // Transforma estos 4 caracteres a un numero
        strcpy(MenReci, buffer);
        Serial.println(MenReci);
        while (Serial.available() > 0) {
         Serial.read();  //Limpia los caracteres siguientes
        }
    }
if (strcmp(MenReci, "watr") == 0) {
    digitalWrite(relay, HIGH); // envia señal alta al relay
  Serial.println("Relay accionado");
  delay(3000);           // 3 segundo
  
  digitalWrite(relay, LOW);  // envia señal baja al relay
  //Serial.println("Relay no accionado");
  delay(1000);   
  //Serial.println("Regando");
  memset(MenReci, 0, sizeof(MenReci)); 
}

if (strcmp(MenReci, "auto") == 0) {
  regadoAuto = !regadoAuto;
  if ( regadoAuto == true){ Serial.println("Modo automatico activado");}
  if ( regadoAuto == false){ Serial.println("Modo automatico desactivado");}
  memset(MenReci, 0, sizeof(MenReci));
}


delay(500); 

  //Regado Automatico
  if ((tBucle - tRegado >= 12000) && (regadoAuto)) { //Determina cada cuando manda un dato de temperatura a la interfaz
    // Manda la data a la interfaz:
    
  digitalWrite(relay, HIGH); // envia señal alta al relay
  //Serial.println("Relay accionado");
  delay(1000);           //1 segundo
  
  digitalWrite(relay, LOW);  // envia señal baja al relay
  //Serial.println("Relay no accionado");
  delay(1000);           // 1 segundo
      tRegado = tBucle; // Actualiza el ultimo tiempo de regado
}



// Leemos la temperatura en grados celsius y la humedad en porcentaje:
float t = dht.readTemperature(); 
float h = dht.readHumidity();
int tInt = int(t);
int hInt = int(h);
String tStr = "t_0" + String(tInt) + "_h_0" + String(hInt); // La convertimos en algo enviable a python

// Comprobamos si ha habido algún error en la lectura 
 //Serial.println(t);
  if (tBucle - tData >= 2000) { //Determina cada cuando manda un dato de temperatura a la interfaz
    // Manda la data a la interfaz:
    
    tData = tBucle; //Actualiza el ultimo tiempo en el que se envio data
   Serial.println(tStr);
    if ( isnan(t)) {
   Serial.println("Error obteniendo los datos del sensor DHT11"); return; } 


}


}