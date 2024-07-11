using System;
using UnityEngine;
using System.IO;
using UnityEditor.Experimental.GraphView;

public class GyroscopeTest : MonoBehaviour
{
    private Gyroscope _gyro;
    private void Start()
    {
        _gyro = Input.gyro;
        _gyro.enabled = true;
        
    }
    
    private void Update()
    {
        Debug.Log(_gyro.attitude);
    }
}
