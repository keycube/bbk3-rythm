using UnityEditor;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Layouts;

namespace Game.CustomLayout
{
    
    [InputControlLayout(stateType = typeof(BBK3HIDInputReport))]
#if UNITY_EDITOR
    [InitializeOnLoad] // Make sure static constructor is called during startup.
#endif
    public class BBK3GamepadHID : InputDevice
    {
        
        static BBK3GamepadHID()
        {
            InputSystem.RegisterLayout<BBK3GamepadHID>(
                matches: new InputDeviceMatcher()
                    .WithInterface("HID")
                    .WithCapability("vendorId", 0x2886)
                    .WithCapability("productId", 0x8045));
        }
        /*
        // In the Player, to trigger the calling of the static constructor,
        // create an empty method annotated with RuntimeInitializeOnLoadMethod.
        [RuntimeInitializeOnLoadMethod] 
        static void Init() {}
        */
    }
}