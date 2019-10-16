# Energize

ING Wholesale Banking Advanced Analytics Experimentation week project: Measure the energy in a meeting room!

## Setup
There are 3 parts to this project:

1. Capture the video feed, call Energy Prediction periodically
2. Based on images received, predict the energy in the room. Call Energy Reporter to report on it
3. Report energy data back to the video conference

![alt text](./docs/img/EnergyMeter.png)

## How to run

Start the prediction server:
```bash
python -m energize.main_server
```

Install extension:
1. Go to `chrome://extensions` and enable development mode
2. Click load unpacked and select the `capture_video_web` folder to install extension
3. Visit `meet.google.com` and click on extension icon to Start

## How to test

If you want to test while the server is running, you can run:
```bash
python ./test/energy_prediction/test_main_server.py
python ./test/energy_prediction/test_main_server_with_camera.py
```
