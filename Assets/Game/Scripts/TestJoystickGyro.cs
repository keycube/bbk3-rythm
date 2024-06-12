using System;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Serialization;

namespace Game.Scripts
{
    public class TestJoystickGyro : MonoBehaviour
    {
        [SerializeField] private InputActionReference gyrscopeX;
        [SerializeField] private InputActionReference gyrscopeY;
        [SerializeField] private InputActionReference gyrscopeZ;
        [SerializeField] private InputActionReference buttonUp;
        [SerializeField] private InputActionReference buttonFront;
        [SerializeField] private InputActionReference buttonBack;
        [SerializeField] private InputActionReference buttonLeft;
        [SerializeField] private InputActionReference buttonRight;
        
        private int currentlyPressed = 0;
        //slider for the gyroscope amplifier
        [Range(0.1f, 10.0f)]
        public float amplifier = 1.0f;
        // Start is called before the first frame update
        void Start()
        {
            gyrscopeX.action.Enable();
            gyrscopeY.action.Enable();
            gyrscopeZ.action.Enable();
            buttonUp.action.Enable();
            buttonFront.action.Enable();
            buttonBack.action.Enable();
            buttonLeft.action.Enable();
            buttonRight.action.Enable();
        }

        private void OnEnable()
        {
            buttonLeft.action.started += OnButtonPressed;
            buttonRight.action.started += OnButtonPressed;
            buttonFront.action.started += OnButtonPressed;
            buttonBack.action.started += OnButtonPressed;
            buttonUp.action.started += OnButtonPressed;
            buttonLeft.action.canceled += OnButtonReleased;
            buttonRight.action.canceled += OnButtonReleased;
            buttonFront.action.canceled += OnButtonReleased;
            buttonBack.action.canceled += OnButtonReleased;
            buttonUp.action.canceled += OnButtonReleased;
        }
        
        private void OnDisable()
        {
            buttonLeft.action.started -= OnButtonPressed;
            buttonRight.action.started -= OnButtonPressed;
            buttonFront.action.started -= OnButtonPressed;
            buttonBack.action.started -= OnButtonPressed;
            buttonUp.action.started -= OnButtonPressed;
            buttonLeft.action.canceled -= OnButtonReleased;
            buttonRight.action.canceled -= OnButtonReleased;
            buttonFront.action.canceled -= OnButtonReleased;
            buttonBack.action.canceled -= OnButtonReleased;
            buttonUp.action.canceled -= OnButtonReleased;
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
            var x = -gyrscopeY.action.ReadValue<float>();
            var y = -gyrscopeX.action.ReadValue<float>();
            var z = gyrscopeZ.action.ReadValue<float>();
            var rot = Quaternion.Euler(x * amplifier, y * amplifier, z * amplifier);
            transform.Rotate(rot.eulerAngles);
        }
    }
}
