using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;

internal struct _DronePosition
{
    internal float _roll;
    internal float _pitch;
    internal float _yaw;

    internal float _x;
    internal float _y;
    internal float _z;

    internal Vector3 _angularPosition;
    internal Vector3 _3dPosition;
}

internal sealed class UpdateDronePosition : MonoBehaviour
{
    GameObject telemetryStats;

    private _DronePosition _positionData;

    void Start()
    {
        GPSEncoder.SetLocalOrigin(new Vector2(52.221317f, 21.005425f));
        telemetryStats = GameObject.Find("DisplayManager");

        _positionData._roll = 0.0f;
        _positionData._pitch = 0.0f;
        _positionData._yaw = 0.0f;

        _positionData._angularPosition = new Vector3(
             _positionData._roll,
             _positionData._yaw,
             _positionData._pitch
            );
    }

    public void UpdatePosition(List<float> angular_position, IPEndPoint ip_addr)
    {
        _positionData._roll = angular_position[0] * 180f / 3.141f;
        _positionData._pitch = angular_position[1] * 180f / 3.141f;
        _positionData._yaw = angular_position[2] * 180f / 3.141f;

        telemetryStats.GetComponent<TelemetryDataDisplayManager>().updateAnglesData(
                _positionData._roll,
                _positionData._pitch,
                _positionData._yaw
            );
        telemetryStats.GetComponent<TelemetryDataDisplayManager>().whoSending(ip_addr);

        _positionData._angularPosition = new Vector3(
            _positionData._roll,
            _positionData._yaw,
            _positionData._pitch
           );

        transform.eulerAngles = _positionData._angularPosition;
    }

    public void UpdatePositionTele(Telemetry angular_position, IPEndPoint ip_addr)
    {
        _positionData._roll = angular_position.roll * 180f / 3.141f;
        _positionData._pitch = angular_position.pitch * 180f / 3.141f;
        _positionData._yaw = angular_position.yaw * 180f / 3.141f;

        
        _positionData._x = angular_position.X; // lat
        _positionData._y = angular_position.Y; // alt
        _positionData._z = angular_position.Z; // long

        telemetryStats.GetComponent<TelemetryDataDisplayManager>().updateAnglesData(
                _positionData._roll,
                _positionData._pitch,
                _positionData._yaw
            );
        telemetryStats.GetComponent<TelemetryDataDisplayManager>().whoSending(ip_addr);

        _positionData._angularPosition = new Vector3(
            _positionData._roll,
            _positionData._yaw,
            _positionData._pitch
           );

        
        _positionData._3dPosition = new Vector3(
           _positionData._x,
           _positionData._y,
           _positionData._z
          );
        Vector3 newPos = GPSEncoder.GPSToUCS(_positionData._3dPosition.x, _positionData._3dPosition.z);
        newPos.y = _positionData._3dPosition.y;

        // Debug.Log(newPos);

        transform.eulerAngles = _positionData._angularPosition;
        transform.position = new Vector3(-newPos.x, newPos.z, newPos.y) / 10.0F; 
    }
}
