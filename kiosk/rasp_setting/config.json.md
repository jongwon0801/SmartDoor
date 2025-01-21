# ~/www/python/config.json
# 차이점

# 192.168.0.161
"pir_inside": {"pin": 14, "times": 30, "isDoorcloserSafeMode": true},

# 192.168.0.139
"pir_inside": {"pin": 25, "times": 30, "isDoorcloserSafeMode": false}


# 192.168.0.161
"doorcloser": {"pin": 21, "safe_pin": 15, "checktimes": 0, "delaytime": 0.2, "isUse": true, "file":"/home/pi/www/sound/open_g10.wav"}

# 192.168.0.139
"doorcloser": {"pin": 23, "safe_pin": 24, "checktimes": 0, "delaytime": 0.2, "isUse": false, "file":"/home/pi/www/sound/open_g10.wav"}


# 192.168.0.161
"doorlock": "/dev/ttyUSB0"

# 192.168.0.139
"doorlock": "/dev/hione"


# 192.168.0.161
"isUseRecord": true

# 192.168.0.139
"isUseRecord": false,


# 192.168.0.161
"outsideSpeakerDevice": {"player":"vlcPlayer", "device":"iec958:CARD=Device,DEV=0", "aout":"alsa"}

# 192.168.0.139
"outsideSpeakerDevice": {"player":"vlcPlayer", "device":"iec958:CARD=Device,DEV=0", "aout":""}



