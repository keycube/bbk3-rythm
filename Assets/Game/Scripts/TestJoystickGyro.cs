using System;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Serialization;

namespace Game.Scripts
{
    public class TestJoystickGyro : MonoBehaviour
    {
        [SerializeField] private InputActionAsset controls;
        
        private Vector3 velocity = Vector3.zero;
        private InputActionMap _sensorsMap;
        
        private int currentlyPressed = 0;
        //slider for the gyroscope amplifier
        [Range(0.1f, 10.0f)]
        public float amplifier = 1.0f;
        // Start is called before the first frame update
        void Start()
        {
            controls.Enable();
            _sensorsMap = controls.actionMaps[1];
        }

        private void OnEnable()
        {
            foreach (var action in controls.actionMaps[0].actions)
            {
                action.started += OnButtonPressed;
                action.canceled += OnButtonReleased;
            }
        }
        
        private void OnDisable()
        {
            foreach (var action in controls.actionMaps[0].actions)
            {
                action.started -= OnButtonPressed;
                action.canceled -= OnButtonReleased;
            }
        }
        
        private void OnButtonPressed(InputAction.CallbackContext ctx)
        {
            currentlyPressed++;
            Debug.Log(currentlyPressed);
            if (currentlyPressed == 5)
            {
                transform.rotation = Quaternion.identity;
            }
        }
        
        private void OnButtonReleased(InputAction.CallbackContext ctx)
        {
            currentlyPressed--;
            Debug.Log(currentlyPressed);
        }

        private void Update()
        {
            var x = _sensorsMap.FindAction("GyroX").ReadValue<float>();
            var y = _sensorsMap.FindAction("GyroY").ReadValue<float>();
            var z = _sensorsMap.FindAction("GyroZ").ReadValue<float>();
            //var rot = Quaternion.Euler(x * amplifier, y * amplifier, z * amplifier);
            var rot = Quaternion.Euler(x * amplifier, y * amplifier, z * amplifier);
            transform.Rotate(rot.eulerAngles);
            Debug.Log(x);
        }

        private void FixedUpdate()
        {
            var accel = new Vector3(_sensorsMap.FindAction("AccelX").ReadValue<float>(), 
                _sensorsMap.FindAction("AccelY").ReadValue<float>(), 
                _sensorsMap.FindAction("AccelZ").ReadValue<float>());
            var gyro = new Vector3(_sensorsMap.FindAction("GyroX").ReadValue<float>(), 
                _sensorsMap.FindAction("GyroY").ReadValue<float>(), 
                _sensorsMap.FindAction("GyroZ").ReadValue<float>());
            //Debug.Log("accel " + accel);
            transform.position = accel;
        }
    }
}
