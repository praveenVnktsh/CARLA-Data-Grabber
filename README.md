# CARLA-Data-Grabber
This is a repository that gets data from the CARLA simulator without affecting the simulation. This helps if you want data to train your Deep Learning model.

## Explanation

Since writing to disk is a task that can be a bottleneck for the simulation, it makes sense not to constantly write to disk at each frame, but to rather store the files to a buffer, and then write when the buffer is full. This repository implements the same idea.

## Usage


Place the two python files in the `PythonClient/` folder of the CARLA simulator and run the following commands.

Open 2 Terminals:

- In terminal 1, run
`.\CarlaUE4.exe /Game/Maps/RaceTrack -windowed -carla-server -benchmark -fps=20`

- In terminal 2, run
`py -3.6 PythonClient/controlManualData.py --images-to-disk --location=data/`


## Notes

If you use a custom racetrack (like the one from the Self Driving Course from Coursera), and don't notice any semantic segmentation output (black), then it is likely that the particular track doesn't have segmentations defined within it. Try some other race track!

### References

This repo is heavily taken from https://sagnibak.github.io/blog/how-to-use-carla/ 