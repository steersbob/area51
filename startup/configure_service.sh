#/bin/bash

sudo chown pi ./startup.sh
sudo chmod +x ./startup.sh
sudo systemctl enable compose_ui.service
sudo systemctl start compose_ui.service
