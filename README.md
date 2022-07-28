# gst-nv-decode-appsink
Hardware accelerated decoding using Nvidia GPUs. Gstreamer is used for media handling in Python

# Dependencies
As long as you run in deepstream container, you don't need any special setup

Python code needs numy and matplotlib can be used for plotting. Run inside container
`python3 -m pip install numpy matplotlib`


# Instructions
- Run the deepstream container (check commands below)
- `cd  gst-nv-decode-appsink`
- `python3 main.py`



## Docker commands
### Run container
```
xhost +
sudo docker run --gpus all -it --name nvdec --net=host --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/minigo/nvdec-demo:/src/nvdec-demo -e DISPLAY=$DISPLAY -w /opt/nvidia/deepstream/deepstream-6.1 nvcr.io/nvidia/deepstream:6.1-devel bash 
```

### go inside running container
```
sudo docker start nvdec
sudo docker exec -it nvdec bash
```

------
Tags
- go2sig--nvdec
