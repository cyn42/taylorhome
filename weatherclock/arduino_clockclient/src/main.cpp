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

Adafruit_NeoPixel grid = Adafruit_NeoPixel(100, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel connectivity_indicator = Adafruit_NeoPixel(2, WIFIPIN, NEO_GRB + NEO_KHZ800);
extern const uint8_t gamma8[];

ESP8266WebServer server(80);
long time = 0;
long lastCheckin = millis();

void setPixelColor(uint16_t pixel, long red, long green, long blue ) {
  uint8_t r = pgm_read_byte(&gamma8[red]);
  uint8_t g = pgm_read_byte(&gamma8[green]);
  uint8_t b = pgm_read_byte(&gamma8[blue]);
  grid.setPixelColor(pixel,grid.Color(r,g,b));
  grid.show();
}

void showOK() {
  connectivity_indicator.setPixelColor(0,connectivity_indicator.Color(0,255,0));
  connectivity_indicator.show();
  lastCheckin = millis();
}

void showError() {
  connectivity_indicator.setPixelColor(0,connectivity_indicator.Color(255,0,0));
  connectivity_indicator.show();
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

void handle_root() {
  server.send(200, "text/plain", "Connection to weather clock succeeded");
  delay(100);
}

void show_icon(uint16_t pixels[], int numPixels) {
   long red_value = random(256);
   long green_value = random(256);
   long blue_value = random(256);

   for (int i=0;i<numPixels;i++) {
     uint16_t pix = pixels[i];
     setPixelColor(pix,red_value, green_value, blue_value);
     //grid.show();
   }
   delay(100);

   showOK();
}

void clear_grid() {
  for(uint16_t i=0; i<grid.numPixels(); i++) {
    grid.setPixelColor(i, (0,0,0));
  }
  grid.show();

  server.send(200, "text/plain", "Grid cleared");
  delay(100);

  showOK();
}

void set_color(long r, long g, long b) {
  //22,23, 37, 36
  Serial.print("Setting color to ");
  Serial.print(r);
  Serial.print(", ");
  Serial.print(g);
  Serial.print(", ");
  Serial.print(b);
  Serial.println(".");

  setPixelColor(22,r,g,b);
  setPixelColor(23,r,g,b);
  setPixelColor(36,r,g,b);
  setPixelColor(37,r,g,b);
  grid.show();

  showOK();


}

void setup() {
  Serial.begin(115200);

  grid.begin();
  grid.setBrightness(64);
  grid.show(); // Initialize all pixels to 'off'

  connectivity_indicator.begin();
  connectivity_indicator.show();

  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.print("\n\r \n\rWorking to connect");
  while (WiFi.status() != WL_CONNECTED) {
    connectivity_indicator.setPixelColor(1,connectivity_indicator.Color(255,100,0));
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
  // Health indicator starts at yellow until first successful display
  connectivity_indicator.setPixelColor(0,connectivity_indicator.Color(255,100,0));
  connectivity_indicator.show();
  // Start the server
  server.on("/", handle_root);

  server.on("/cleargrid", clear_grid);

  server.on("/icon", HTTP_POST, [](){
    StaticJsonBuffer<200> newBuffer;
    JsonObject& newjson = newBuffer.parseObject(server.arg("plain"));
    const char* icon = newjson["icon"];
    Serial.print("Showing icon ");
    Serial.println(icon);
    int _numpixels = newjson["numpixels"];
    uint16_t pixels[_numpixels];
    for (int i=0;i<_numpixels;i++) {
      uint16_t pixelLoc = newjson["pixels"][i];
      pixels[i] = pixelLoc;
    }
    show_icon(pixels,_numpixels);
    server.send ( 200, "text/plain", "{success:true}" );
    });

    server.on("/color", HTTP_POST, [](){
      Serial.println("Color service triggered");
      StaticJsonBuffer<200> newBuffer;
      JsonObject& newjson = newBuffer.parseObject(server.arg("plain"));
      int red = newjson["red"];
      int green = newjson["green"];
      int blue = newjson["blue"];
      set_color(red, green, blue);
      server.send(200, "text/plain", "Color displayed");
      delay(100);
      });

  server.begin();

  // Peace of mind: All of the pixels work
  colorWipe(grid.Color(255, 0, 0), 50); // Red

}



void loop() {
  server.handleClient();
  if (millis() > time+ 1000) {
        time = millis();

        if (millis() > lastCheckin + 600000 ) {
          showError();
        }

        delay(100);
  }

}

const uint8_t PROGMEM gamma8[] = {
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 };
