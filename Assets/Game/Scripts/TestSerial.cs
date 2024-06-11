using System.IO.Ports;
using UnityEngine;

namespace Game.Scripts
{
    public class TestSerial : MonoBehaviour
    {
        private SerialPort sp;
        // Start is called before the first frame update
        void Start()
        {
            sp = new SerialPort("COM8", 9600);
            sp.Open();
            sp.ReadTimeout = 500;
        }

        // Update is called once per frame
        void Update()
        {
            Debug.Log(sp.ReadByte());
        }
    }
}
