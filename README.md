# Drone Positioning
## Project overview
The main goal was to develop reliable service for communicating with drone via MAVlink protocol to send through this service GPS coordinates and angular position of a UAV to the HoloLens2 system by UDP.
## Project structure
The project consists of two main subsystems:
- Python-based server that receives data from a UAV and sends them to HL2, check  ```/PositionServer```
- Unity app running on HL2, which receives coordinates and tries to visualize a drone as a cube in space, check  ```/UnityClient```
## Setup
### PositionServer
In the direcotry ```/PositionServer``` there is a python server. Below there is presented a quick overview of dependencies required to run it:
| Dependency | Version |
|---------:|-----------|
| Python   | 3.7.15    |
| pymavlink| 2.4.37    |
| pyserial | 3.5       |

For installing ```pymavlink``` please refer to: https://pypi.org/project/pymavlink/
The environment for this part of the project was created with ```anaconda``` and it is by far the most convenient.
### UnityClient
In the directory ```/UnityCLient``` there is a Unity project which after compilation on HL2 serves as the main appliction.
| Dependency   | Version     |
|-------------:|-------------|
| Unity Engine | 2020.3.42f1 |
| Visual Studio| 2019        |

Try sticking to the version of Unity Engine mentioned above as some bugs of versions older than this one made the project not working properly.
## How to start
### Position Client
The main file is ```serverStart.py``` to launch the server use:

```python3 serverStart.py --latitude [float] --longtitude [float] --altitude [float]```

The flag ```--altitude``` is not mandatory, if not given then ```altitude=100 [m]```. The mentioned arguments are GPS position of a UAV operator that are fixed (the operator is assumend to not be moving).

***It is crucial*** to complete properly JSON file ```/data/connection_data.json``` with necessary infomration!
```json
{
	"localHostIP": "xxx.xxx.x.xxx", 
	"remoteIP": "xxx.xxx.x.xxx",
	"port": 55555,
	"dataBufferSize": 4096
}
```

- ```localHostIP```: machine on which server runs
- ```remoteIP```: ip assigned to HL2
- ```port```: the port number which was allowed to transfer data out of local machine

### UnityClient
For building and deploying Unity app to HL2 please refer to the following resiurces:
- https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/build-and-deploy-to-hololens
- https://learn.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/using-visual-studio?tabs=hl2

***Disclaimer***: no settings of the current project available here should be changed!

After succesfull build and deployment:
1. Turn on the UAV, make sure it transmits the data
2. Connect all devices to the same network (no internet access required)
3. Launch  ```startServer.py```
4. Launch Unity app from HL2

The Unity app can also work inside the editor. In this case no build is required, simply click on the launch button (make sure the steps 1, 2 and 3 have been executed before).

## Testing & troubleshooting
The system was tested on the following scenarios:
- Debian 11 machine as PositionServer and HL2 as UnityClient
- Debian 11 machine as PositionServer and Win10 machine with Unity Editor running app as UnityClient

### Possible problems
1. The algorithm for calculating distance based on GPS coorindates is not very accurate and there are still unresolved problems with it displaying correct position. To test only angular position comment out line 77 and 80 from ```serverStart.py``` so server sends only angular positions.
2. Different machines assign radio modem to different ports, if any problems occur with connection try using MissonPlanner to check which port is used. Lines from 29 to 33 in ```serverStart.py``` should check whether the server machine is Linux or Windows.
3. It is unresolved why when Unity app runs on HL2 the scene is not fixed in place but moves with a user head.
