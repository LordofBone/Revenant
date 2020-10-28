// Thanks to https://create.arduino.cc/projecthub/whimsy-makerspace/arduino-compatible-nano-neopixel-controller-6f0c4b?ref=user&ref_id=74654&offset=1
// for the Neopixel controls

#include <Servo.h>
#include <Adafruit_NeoPixel.h>

int dataPin = 7;  // Arduino PWM data pin D6
int pixels = 16;  // Number of Neopixels

// LED Pin setup; I'm using a Red/Blue combo LED here
int redPin = 13;  // Red LED Pin
int bluePin = 8;  // Blue LED Pin

// Parameter 1 = Number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = Pixel type flags, add together as needed:
Adafruit_NeoPixel strip = Adafruit_NeoPixel(pixels, dataPin, NEO_GRB + NEO_KHZ800);

// Servos setup
Servo servo1;
int pos = 0;
int mouthWait = 200;

// String for incoming commands from serial
String incoming;

void setup() {
  Serial.begin(115200);

  // Neopixel setup
  strip.begin();
  strip.show();

  // Servo config, set to close position
  servo1.attach(12);
  servo1.writeMicroseconds(pos);
  delay(2000);

  // LED Pin setup
  pinMode(redPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void openMouth() {
  // Set servo to open mouth position
  servo1.writeMicroseconds(1500);
  delay(mouthWait);
}

void closeMouth() {
  // Set servo to closed mouth position
  servo1.writeMicroseconds(0);
  delay(mouthWait);
}

void shoulderRocket() {
  // Activate shoulder rocket
  theaterChaseRainbow(50);
  delay(2000);
}

void redEye() {
  // Toggle Red LED
  digitalWrite(redPin, !digitalRead(redPin));
}

void blueEye() {
  // Toggle Blue LED
  digitalWrite(bluePin, !digitalRead(bluePin));
}

void testMouthRun() {
  // Make the mouth open and close 10 times as a test
  mouthMover(10);
}

void mouthMover(int mouthMoves) {
  // Make the mouth servers open and close a set number of times
  for (int i = 0; i <= mouthMoves; i++) {
    openMouth();
    closeMouth();
  }
}

// This is the command processor that will take in serial inputs and select the correct functions based on the input
void runCommand(String command) {
  Serial.println("Running command: ");
  Serial.println(command);

  if (command == "run_test_mouth") {
    testMouthRun();
  }
  else if (command == "open_mouth") {
    openMouth();
  }
  else if (command == "close_mouth") {
    closeMouth();
  }
  else if (command == "fire_shoulder_rocket") {
    shoulderRocket();
  }
  else if (command == "red_eye_toggle") {
    redEye();
  }
  else if (command == "blue_eye_toggle") {
    blueEye();
  }
  else if (command == "test_serial") {
    Serial.println("SUCCESS!");
  }
  else {
    Serial.println("unknown_command");
  }
}

void loop() {
  // While serial available take in incoming commands
  while (Serial.available()) {
    // Grab incoming serial from usb until carriage return
    incoming = Serial.readStringUntil('\n');
    // Send comand to command processor
    runCommand(incoming);
  }
}


// Below is extra LED patterns from https://create.arduino.cc/projecthub/whimsy-makerspace/arduino-compatible-nano-neopixel-controller-6f0c4b?ref=user&ref_id=74654&offset=1
// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for (j = 0; j < 256; j++) {
    for (i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for (j = 0; j < 256 * 5; j++) { // 5 cycles of all colors on wheel
    for (i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j = 0; j < 10; j++) { //do 10 cycles of chasing
    for (int q = 0; q < 3; q++) {
      for (int i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, c);  //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (int i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, 0);      //turn every third pixel off
      }
    }
  }
}

// Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j = 0; j < 256; j++) {   // cycle all 256 colors in the wheel
    for (int q = 0; q < 3; q++) {
      for (int i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, Wheel( (i + j) % 255)); //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (int i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, 0);      //turn every third pixel off
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else if (WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  } else {
    WheelPos -= 170;
    return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
}
