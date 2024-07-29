#include "Adafruit_TinyUSB.h"
#include <Adafruit_NeoPixel.h>
#include "LSM6DS3.h"

#define WHITE 0xCCCCCC
#define BLACK 0x000000
#define MAGENTA 0xFF00FF
#define GREEN 0x33FF33


enum
{
  RID_GAMEPAD = 1,
  RID_KEYBOARD,
};
// HID report descriptor using TinyUSB's template
// Single Report (no ID) descriptor
uint8_t const desc_hid_report[] =
{
  TUD_HID_REPORT_DESC_KEYBOARD( HID_REPORT_ID(RID_KEYBOARD) ),
  TUD_HID_REPORT_DESC_GAMEPAD( HID_REPORT_ID(RID_GAMEPAD) )
};

uint8_t available_keys[5] = { HID_KEY_W, HID_KEY_A, HID_KEY_S, HID_KEY_D, HID_KEY_X };
bool btn_pressed = false;
bool btn_pressed_prev = false;
bool keyboard_mode = false;
bool all_prev_pressed = false;
int num_button_pressed = 0;
int switch_time = 5000;

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
  uint8_t keycodes[6] = { 0 };
  num_button_pressed = 0;

  // scan active pins and add inputs in buffer
  for(uint8_t i=0; i < pincount; i++)
  {
    if ( activeState == digitalRead(pins[i]) )
    {
      num_button_pressed += 1;
      // if pin is active, add the button in the buffer (either in keyboard or gamepad mode)
      if(keyboard_mode){
        keycodes[i] = available_keys[i];
        btn_pressed = true;
        btn_pressed_prev = true;
      }
      else
        gp.buttons |= 1U << i;
      
      pixels.setPixelColor(i, WHITE);
    }
    else{
      pixels.setPixelColor(i, colorsHex[i]);
    }
  }
  pixels.show();
  
  // check if all buttons are pressed, if so, update the countdown
  if(num_button_pressed == 5){
    all_prev_pressed = true;
    switch_time -= 10;

    // if countdown reaches 0, switch to keyboard mode
    if (switch_time <= 0){
      keyboard_mode = !keyboard_mode;
      pixels.fill(BLACK);
    }
  }
  // reset all if buttons released
  else if (num_button_pressed != 5 && all_prev_pressed){
    switch_time = 5000;
    all_prev_pressed = false;
  }


  
  // send the keyboard report if a button has been pressed
  if(btn_pressed == true){
    if(keyboard_mode)
      usb_hid.keyboardReport(RID_KEYBOARD, 0, keycodes);
    btn_pressed = false;
  }
  // send one release report and avoid useless reports
  else if(btn_pressed == false && btn_pressed_prev == true){
    if(keyboard_mode)
      usb_hid.keyboardRelease(RID_KEYBOARD);
    btn_pressed_prev = false;
  }


  // wake up host if we are in suspend mode
  if ( TinyUSBDevice.suspended())
  {
    
    TinyUSBDevice.remoteWakeup();
  }
  
  // reading all IMU values as joystick inputs
  gp.x = myIMU.readFloatGyroX()/10;
  gp.y = myIMU.readFloatGyroY()/10;
  gp.z = myIMU.readFloatGyroZ()/10;
  
  gp.rx = myIMU.readFloatAccelX()*10;
  gp.ry = myIMU.readFloatAccelY()*10;
  gp.rz = myIMU.readFloatAccelZ()*10;

  // send gamepad report
  usb_hid.sendReport(RID_GAMEPAD, &gp, sizeof(gp));
}
