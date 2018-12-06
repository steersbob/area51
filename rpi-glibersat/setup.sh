#! /usr/bin/env bash

mkdir ./app
echo '{"dashboards":[],"dashboard-items":[],"services":[]}' > app/datastore.json
echo "[]" > app/brewblox_db.json
echo "{}" > app/brewblox_config.json