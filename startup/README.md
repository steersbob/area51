# Running a startup script on Raspberry Pi

Source: https://raspberrypi.stackexchange.com/questions/78991/running-a-script-after-an-internet-connection-is-established

## Create Service

```
sudo systemctl edit --force --full compose_ui.service
```

Now paste the contents of `compose_ui.service`, and exit with saving.

## Add startup file

Copy `startup.sh` and `configure_service.sh` to the user root on the raspberry (`~/`)

## Configure service

Run `configure_service.sh` and reboot
