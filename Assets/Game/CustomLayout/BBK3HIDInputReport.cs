// We receive data as raw HID input reports. This struct
// describes the raw binary format of such a report.

using System.Runtime.InteropServices;
using UnityEngine.InputSystem.Layouts;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.InputSystem.Utilities;

namespace Game.CustomLayout
{
    [StructLayout(LayoutKind.Explicit, Size = 32)]
    struct BBK3HIDInputReport : IInputStateTypeInfo
    {
        // Because all HID input reports are tagged with the 'HID ' FourCC,
        // this is the format we need to use for this state struct.
        public FourCC format => new FourCC('H', 'I', 'D');

        // HID input reports can start with an 8-bit report ID. It depends on the device
        // whether this is present or not. On the PS4 DualShock controller, it is
        // present. We don't really need to add the field, but let's do so for the sake of
        // completeness. This can also help with debugging.
        //[FieldOffset(0)] public byte reportId;
        
        // The InputControl annotations here probably look a little scary, but what we do
        // here is relatively straightforward. The fields we add we annotate with
        // [FieldOffset] to force them to the right location, and then we add InputControl
        // to attach controls to the fields. Each InputControl attribute can only do one of
        // two things: either it adds a new control or it modifies an existing control.
        // Given that our layout is based on Gamepad, almost all the controls here are
        // inherited from Gamepad, and we just modify settings on them.
        
        // X & Y
        [InputControl(name = "leftStick", layout = "Stick", format = "VEC2", sizeInBits = 32)]
        [InputControl(name = "leftStick/x", offset = 0, format = "SHRT", sizeInBits = 16,
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=1")]
        [InputControl(name = "leftStick/left", offset = 0, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=0.0,invert")]
        [InputControl(name = "leftStick/right", offset = 0, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=0.0,clampMax=1")]
 
        [InputControl(name = "leftStick/y", offset = 1, format = "SHRT", sizeInBits = 16,
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=1")]
        [InputControl(name = "leftStick/down", offset = 1, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=0,clampMax=1")]
        [InputControl(name = "leftStick/up", offset = 1, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=0,invert")]
        [FieldOffset(0)] public byte leftStickX; // Gyro X
        [FieldOffset(1)] public byte leftStickY; // Gyro Y
        
        // Z & RX
        [InputControl(name = "leftLowerStick", layout = "Stick", format = "VEC2", sizeInBits = 32)]
        [InputControl(name = "leftLowerStick/x", offset = 0, displayName = "Left Base X", format = "SHRT", sizeInBits = 16,  parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=1")]
        [InputControl(name = "leftLowerStick/right", layout = "Button", offset = 0, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=0,clampMax=1")]
        [InputControl(name = "leftLowerStick/left", layout = "Button", offset = 0, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=0,invert")]
        [FieldOffset(2)] public byte leftLowerStickX; // Gyro Z
       
        [InputControl(name = "leftLowerStick/y", offset = 1, displayName = "Left Base Y", format = "SHRT", sizeInBits = 16,  parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=1")]
        [InputControl(name = "leftLowerStick/up",  offset = 1, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=0,clampMax=1")]
        [InputControl(name = "leftLowerStick/down",  offset = 1, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=0,invert")]
        [FieldOffset(3)] public byte leftLowerStickY; // Accel Z
     
        // ry & rz
        [InputControl(name = "rightStick", layout = "Stick", format = "VEC2", sizeInBits = 32)]
        [InputControl(name = "rightStick/x", offset = 0,  displayName = "Right Upper X", format = "SHRT", sizeInBits = 16,  parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=1")]
        [InputControl(name = "rightStick/right", layout = "Button", offset = 0, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=0,clampMax=1")]
        [InputControl(name = "rightStick/left", layout = "Button", offset = 0, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=0,invert")]
        [FieldOffset(4)] public byte rightStickX; // Accel X
     
        [InputControl(name = "rightStick/y",     offset = 1, displayName = "Right Upper Y", format = "SHRT", sizeInBits = 16, parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=1")]
        [InputControl(name = "rightStick/down", layout = "Button", offset = 1, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=0,clampMax=1")]
        [InputControl(name = "rightStick/up", layout = "Button", offset = 1, format = "BYTE",
            parameters = "normalize,normalizeMin=-1,normalizeMax=1,normalizeZero=0.0,clamp,clampMin=-1,clampMax=0,invert")]
        [FieldOffset(5)] public byte rightStickY; // Accel Y
        
        // Buttons
        [InputControl(name = "buttonWest", layout = "Button", displayName = "B1", bit = 7)]
        [InputControl(name = "buttonSouth", layout = "Button", displayName = "B2", bit = 6)]
        [InputControl(name = "buttonEast", layout = "Button", displayName = "B3", bit = 5)]
        [InputControl(name = "buttonNorth", layout = "Button", displayName = "B4", bit = 4)]
        [InputControl(name = "leftShoulder", layout = "Button", displayName = "B5", bit = 3)]
        [FieldOffset(7)] public byte buttons;
    }
}