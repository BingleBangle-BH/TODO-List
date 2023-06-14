# syntax=docker/dockerfile:1
   
FROM dokken/ubuntu-20.04
WORKDIR /TODO-LIST
RUN sudo apt update
RUN sudo apt install build-essential -y
RUN sudo apt install --assume-yes git clang curl libssl-dev llvm libudev-dev make protobuf-compiler -y
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN . $HOME/.cargo/env

# RUN sudo apt-get install adduser libfontconfig1 -y
# RUN wget https://dl.grafana.com/oss/release/grafana_9.5.3_amd64.deb
# RUN sudo dpkg -i grafana_9.5.3_amd64.deb

RUN sudo apt install software-properties-common -y 
RUN sudo add-apt-repository ppa:deadsnakes/ppa -y 
RUN sudo apt install python3.8 -y 
RUN sudo apt install python3-pip -y && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip3 install -r requirements.txt 
RUN chmod +x job_controls.sh
# RUN rustup default stable
# RUN rustup update
# RUN rustup update nightly
# RUN rustup target add wasm32-unknown-unknown --toolchain nightly
# RUN rustup default nightly
# RUN cd substrate-node-template && cargo build --release
# RUN rustup default stable
# RUN cd todo_list && cargo contract build

EXPOSE 5000 8000 9944 3000 9090 9615
CMD ["./job_controls.sh"]