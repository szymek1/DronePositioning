using UnityEngine;
using UnityEngine.UI;
using System.Net;

internal sealed class TelemetryDataDisplayManager : MonoBehaviour
{
    [SerializeField] private Text rollData;
    [SerializeField] private Text pitchData;
    [SerializeField] private Text yawData;

    [SerializeField] private Text serverInfo;

    private float _rollAng;
    private float _pitchAng;
    private float _yawAng;

    private string _serverIP;

    void Start()
    {
        _rollAng = 0.0f;
        _pitchAng = 0.0f;
        _yawAng = 0.0f;
        _serverIP = "0.0.0.0";
    }

    public void updateAnglesData(float rollAngle, float pitchAngle, float yawAngle)
    {
        _rollAng = rollAngle;
        _pitchAng = pitchAngle;
        _yawAng = yawAngle;
    }

    public void whoSending(IPEndPoint ip_addr)
    {
        _serverIP = ip_addr.ToString();
    }

    void Update()
    {
        rollData.text = "Roll: " + _rollAng + " °";
        pitchData.text = "Pitch: " + _pitchAng + " °";
        yawData.text = "Yaw: " + _yawAng + " °";

        serverInfo.text = _serverIP;
    }
}
