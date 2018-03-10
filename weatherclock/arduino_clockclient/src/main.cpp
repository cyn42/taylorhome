#include <Arduino.h>

#include <Adafruit_NeoPixel.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <cfg.h>
#include <ArduinoJson.h>

#define PIN 14
#define WIFIPIN 12
const char* ssid = WIFISSID;
const char* password = WIFIPASSWORD;

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel grid = Adafruit_NeoPixel(100, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel connectivity_indicator = Adafruit_NeoPixel(2, WIFIPIN, NEO_GRB + NEO_KHZ800);

ESP8266WebServer server(80);

void handle_root() {
  server.send(200, "text/plain", "Hello from the weatherclock");
  delay(100);
}

void show_icon(int pixels[], int numPixels) {
  for (int i=0;i<numPixels;i++) {
    //int pixelLoc = newjson["pixels"][i];
    Serial.println(pixels[i]);
  }
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<grid.numPixels(); i++) {
    if (i<6 ) {
      grid.setPixelColor(i, c);
      grid.show();
    } else {
      grid.setPixelColor(i-5, (0,0,0));
      grid.setPixelColor(i, c);
      grid.show();
    }
    delay(wait);
  }
  for(uint16_t i=0; i<grid.numPixels(); i++) {
    grid.setPixelColor(i, (0,0,0));
  }
  grid.show();
}

void setup() {
  Serial.begin(115200);

  grid.begin();
  grid.show(); // Initialize all pixels to 'off'

  connectivity_indicator.begin();
  connectivity_indicator.show();

  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.print("\n\r \n\rWorking to connect");
  while (WiFi.status() != WL_CONNECTED) {
    connectivity_indicator.setPixelColor(1,(255,0,0));
    connectivity_indicator.show();
    delay(250);
    connectivity_indicator.setPixelColor(1,(0,0,0));
    connectivity_indicator.show();
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WeatherClock Client");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  connectivity_indicator.setPixelColor(1,(0,0,255));
  connectivity_indicator.show();
  // Start the server
  server.on("/", handle_root);

  server.on("/json/test", HTTP_POST, [](){
    StaticJsonBuffer<200> newBuffer;
    JsonObject& newjson = newBuffer.parseObject(server.arg("plain"));
    const char* icon = newjson["icon"];
    Serial.println();
    Serial.println(icon);
    Serial.print("Number of pixels to light up: ");
    int _numpixels = newjson["numpixels"];
    int pixels[_numpixels];
    for (int i=0;i<_numpixels;i++) {
      int pixelLoc = newjson["pixels"][i];
      pixels[i] = pixelLoc;
    }
    show_icon(pixels,_numpixels);
    server.send ( 200, "text/plain", "{success:true}" );
    });

  server.begin();

  colorWipe(grid.Color(255, 0, 0), 50); // Red

}



void loop() {
  server.handleClient();
}
