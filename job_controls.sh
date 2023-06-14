#!/bin/bash

# Start 
source $HOME/.cargo/env
rustup default stable
rustup update
rustup update nightly
rustup target add wasm32-unknown-unknown --toolchain nightly
rustup toolchain install nightly-2023-01-01
rustup default nightly-2023-01-01
rustup component add rust-src
cargo install --force --locked cargo-contract@2.0.0
cd /TODO-LIST/todo_list && cargo contract build
rustup default nightly
cd /TODO-LIST/substrate-node-template && cargo build --release


# check is metadata exist
if [ -f "/TODO-LIST/todo_list/ink/metadata.json" ]; then
    mv "metadata.json" "todo_list.json"
fi

# turn on bash's job control
set -m

# Start flask api
cd /TODO-LIST && python3 template/app.py &

# Start blockchain dev mode
cd /TODO-LIST && ./substrate-node-template/target/release/node-template --dev &

# Start http server
cd /TODO-LIST/docs && python3 -m http.server &

# Start prometheus
cd /TODO-LIST/prometheus && ./prometheus --config.file prometheus.yml &

# Start setup
sleep 10
python3 /TODO-LIST/template/main.py &


# wget https://github.com/prometheus/prometheus/releases/download/v2.45.0-rc.0/prometheus-2.45.0-rc.0.linux-amd64.tar.gz
# sudo apt-get install -y adduser libfontconfig1

# sudo systemctl start grafana-server


# docker run -p 5000:5000 -p 8000:8000 -p 9090:9090 -p 9615:9615 --name mycontainer -d -t skyareblue/todolist:1.1
# docker run --name mycontainer -d -i -t todolist:1.0 /bin/sh
# docker exec -it mycontainer sh
# docker system prune --all --force
# now we bring the primary process back into the foreground
# and leave it there
fg %1