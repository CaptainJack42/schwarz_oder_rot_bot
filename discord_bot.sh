#! /bin/sh

### BEGIN INIT INFO
# Provides:          fancontrol.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# Carry out specific functions when asked to by the system

case "$1" in
    start)
        echo "Starting Discord Bot"
        /home/pi/schwarz_oder_rot_bot/main.py & 
        ;;
    stop)
        echo "Stopping Discord Bot"
        pkill -f /home/pi/schwarz_oder_rot_bot/main.py
        ;;
    *)
        echo "Usage: /etc/init.d/discord_bot.sh {start|stop}"
        exit 1
        ;;
esac

exit 0
