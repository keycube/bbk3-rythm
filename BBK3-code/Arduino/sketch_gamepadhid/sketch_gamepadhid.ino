#include "Adafruit_TinyUSB.h"
#include <Adafruit_NeoPixel.h>
#include "LSM6DS3.h"

#define WHITE 0xCCCCCC
#define BLACK 0x000000
#define MAGENTA 0xFF00FF
#define GREEN 0x33FF33


// HID report descriptor using TinyUSB's template
// Single Report (no ID) descriptor
uint8_t const desc_hid_report[] =
{
  TUD_HID_REPORT_DESC_GAMEPAD()
};

// USB HID object. For ESP32 these values cannot be changed after this declaration
// desc report, desc len, protocol, interval, use out endpoint
Adafruit_USBD_HID usb_hid(desc_hid_report, sizeof(desc_hid_report), HID_ITF_PROTOCOL_NONE, 2, false);
hid_gamepad_report_t    gp;

// USB HID object. For ESP32 these values cannot be changed after this declaration
// desc report, desc len, protocol, interval, use out endpoint
LSM6DS3 myIMU(I2C_MODE, 0x6A); 


//------------- Input Pins -------------//
// Array of pins and its keycode.
// Notes: these pins can be replaced by PIN_BUTTONn if defined in setup()
#ifdef ARDUINO_ARCH_RP2040
  uint8_t pins[] = { D1, D2, D3, D4, D5 };
#else
  uint8_t pins[] = { A1, A2, A3, A4, A5 };
#endif

// number of pins
uint8_t pincount = sizeof(pins);

// For keycode definition check out https://github.com/hathach/tinyusb/blob/master/src/class/hid/hid.h
//uint8_t hidcode[] = { HID_KEY_W, HID_KEY_A, HID_KEY_S, HID_KEY_D, HID_KEY_X };

int colorsHex[] = { MAGENTA, MAGENTA, MAGENTA, 0x33FF33, BLACK};

#if defined(ARDUINO_SAMD_CIRCUITPLAYGROUND_EXPRESS) || defined(ARDUINO_NRF52840_CIRCUITPLAY) || defined(ARDUINO_FUNHOUSE_ESP32S2)
  bool activeState = true;
#else
  bool activeState = false;
#endif

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(5, 0, NEO_GRB + NEO_KHZ800);

// the setup function runs once when you press reset or power the board
void setup()
{
  // neopixel if existed
#ifdef PIN_NEOPIXEL
  pixels.begin();
  pixels.setBrightness(50);
#endif
  // Set up pin as input
  for (uint8_t i=0; i<pincount; i++)
  {
    pinMode(pins[i], activeState ? INPUT_PULLDOWN : INPUT_PULLUP);
  }

#if defined(ARDUINO_ARCH_MBED) && defined(ARDUINO_ARCH_RP2040)
  // Manual begin() is required on core without built-in support for TinyUSB such as mbed rp2040
  TinyUSB_Device_Init(0);
#endif

  Serial.begin(9600);
  
  usb_hid.setPollInterval(10);
  usb_hid.setReportDescriptor(desc_hid_report, sizeof(desc_hid_report));

  usb_hid.begin();

  myIMU.begin();

  // wait until device mounted
  while( !TinyUSBDevice.mounted() ) {
    delay(1);
  }
  Serial.flush();
}


void loop()
{
  // poll gpio once each 10 ms
  delay(10);

  // scan active pins and store inputs in the buffer
  for(uint8_t i=0; i < pincount; i++)
  {
    gp.buttons &= ~(1U << i);
    pixels.setPixelColor(i, colorsHex[i]);
    if ( activeState == digitalRead(pins[i]) )
    {
      gp.buttons |= 1U << i;
      pixels.setPixelColor(i, WHITE);
    }
  }
  pixels.show();

  if ( TinyUSBDevice.suspended())
  {
    TinyUSBDevice.remoteWakeup();
  }

  // skip if hid is not ready e.g still transferring previous report
  if ( !usb_hid.ready() ) return;

  // get values from the IMU and turn them into joystick inputs
  gp.x = myIMU.readFloatGyroX()/10;
  gp.y = myIMU.readFloatGyroY()/10;
  gp.z = myIMU.readFloatGyroZ()/10;

  gp.rx = myIMU.readFloatAccelX()*10;
  gp.ry = myIMU.readFloatAccelY()*10;
  gp.rz = myIMU.readFloatAccelZ()*10;
  
  // send gamepad report
  usb_hid.sendReport(0, &gp, sizeof(gp));
}

