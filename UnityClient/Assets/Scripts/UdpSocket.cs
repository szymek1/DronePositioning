using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using System.Text;
using System.Net;
using System.Linq;
using System.Net.Sockets;
using System.Threading;


internal sealed class Telemetry
{
    public Telemetry(ref byte[] receiveBytes)
    {
        // angular positions
        roll = System.BitConverter.ToSingle(receiveBytes, 0);
        pitch = System.BitConverter.ToSingle(receiveBytes, sizeof(float));
        yaw = System.BitConverter.ToSingle(receiveBytes, 2 * sizeof(float));

        // 3d positions
        X = System.BitConverter.ToSingle(receiveBytes, 3 * sizeof(float));
        Y = System.BitConverter.ToSingle(receiveBytes, 4 * sizeof(float));
        Z = System.BitConverter.ToSingle(receiveBytes, 5 * sizeof(float));
    }
    internal float roll { get;}
    internal float pitch { get; }
    internal float yaw { get; }

    
    internal float X { get; }
    internal float Y { get; }
    internal float Z { get; }
}

internal sealed class UdpSocket : MonoBehaviour
{
    [SerializeField] int serverPort = 55555;

    private GameObject _drone;
    private UpdateDronePosition _dronePosUpdater;
    private Telemetry _droneTelemetry;

    private static UdpClient _client;
    private Thread _receiveThread;

    static readonly object lockObject = new object();

    //private List<float> _coordinatesList = new List<float>();
    private bool _processData = false;

    IPEndPoint remoteIPendPoint;

    void Awake()
    {

        _receiveThread = new Thread(new ThreadStart(ReceiveData));
        _receiveThread.Start();
    }

    private void Start() 
    {
        _drone = GameObject.Find("Drone");
        _dronePosUpdater = _drone.GetComponent<UpdateDronePosition>();
    }

    void Update()
    {
        if (_processData)
        {
            lock (lockObject)
            {
                _processData = false;
                //drone.GetComponent<UpdateDronePosition>().UpdatePosition(_coordinatesList, remoteIPendPoint);
                //_dronePosUpdater.UpdatePosition(_coordinatesList, remoteIPendPoint);
                _dronePosUpdater.UpdatePositionTele(_droneTelemetry, remoteIPendPoint);
                //_coordinatesList.Clear();
            }
        }
    }

    private void ReceiveData()
    {

        _client = new UdpClient(serverPort);
        remoteIPendPoint = new IPEndPoint(IPAddress.Loopback, serverPort);
        while (true)
        {
            byte[] receiveBytes = _client.Receive(ref remoteIPendPoint);

            lock (lockObject)
            {
                /*
                _coordinatesList.Add(System.BitConverter.ToSingle(receiveBytes, 0));
                _coordinatesList.Add(System.BitConverter.ToSingle(receiveBytes, sizeof(float)));
                _coordinatesList.Add(System.BitConverter.ToSingle(receiveBytes, 2 * sizeof(float)));*/
                _droneTelemetry = new Telemetry(ref receiveBytes);
                /*
                if (_coordinatesList.Any() != false)
                {
                    _processData = true;
                }*/
                if (_droneTelemetry != null)
                {
                    _processData = true;
                }
            }
        }
    }

    void OnDisable()
    {
        if (_receiveThread != null)
            _receiveThread.Abort();

        _client.Close();
    }

}