# pproxy

## Usage

```
usage: proxy.py [-h] [-ti TARGET_IP] [-tp TARGET_PORT]
                [-li LISTEN_IP] [-lp LISTEN_PORT]
                [-pi PLUGINS_IN] [-po PLUGINS_OUT] [-v]

Simple proxy servie for data interception and modification.
Select plugins to handle the intercepted traffic.

optional arguments:
  -h, --help            show this help message and exit
  -ti TARGET_IP, --targetip TARGET_IP
                        remote target IP or host name
  -tp TARGET_PORT, --targetport TARGET_PORT
                        remote target port
  -li LISTEN_IP, --listenip LISTEN_IP
                        IP address/host name to listen for
                        incoming data
  -lp LISTEN_PORT, --listenport LISTEN_PORT
                        port to listen on
  -pi PLUGINS_IN, --pluginsin PLUGINS_IN
                        comma-separated list of plugins to
                        modify data received from the remote
                        target.
  -po PLUGINS_OUT, --pluginsout PLUGINS_OUT
                        comma-separated list of plugins to
                        modify data before sending to remote
                        target.
  -v, --verbose         More verbose output of status
                        information

```
