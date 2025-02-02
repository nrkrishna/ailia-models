# ailia MODELS tutorial

## Requirements

- Python 3.6 and later

## Install ailia SDK

- [Download a free evaluation version of ailia SDK](https://ailia.jp/en/trial)
- Unzip ailia SDK
- Run the following command

```
cd ailia_sdk/python
python3 bootstrap.py
pip3 install .
```

- In the evaluation version, place the license file in the same folder as libailia.dll ([python_path]/site_packages/ailia) on Windows and in ~/Library/SHALO/ on Mac.

- You can find the location of Python site-packages directory using the following command.

```
pip3 show ailia
```

## Install required libraries for Python

### For Windows, Mac and Linux

```
pip install -r requirements.txt
```

### For Jetson

```
sudo apt install python3-pip
sudo apt install python3-matplotlib
sudo apt install python3-scipy
pip3 install cython
pip3 install numpy
```

[OpenCV for python3 is pre-installed on Jetson.](https://forums.developer.nvidia.com/t/install-opencv-for-python3-in-jetson-nano/74042/3) You only need to run this command if you get a cv2 import error.

```
sudo apt install nvidia-jetpack
```

### For Raspberry Pi

```
pip3 install numpy
pip3 install opencv-python
pip3 install matplotlib
pip3 install scikit-image
sudo apt-get install libatlas-base-dev
```

## Options

The following options can be specified for each model.

```
optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE/VIDEO, --input IMAGE/VIDEO
                        The default (model-dependent) input data (image /
                        video) path. If a directory name is specified, the
                        model will be run for the files inside. File type is
                        specified by --ftype argument (default: lenna.png)
  -v VIDEO, --video VIDEO
                        You can convert the input video by entering style
                        image.If the int variable is given, corresponding
                        webcam input will be used. (default: None)
  -s SAVE_PATH, --savepath SAVE_PATH
                        Save path for the output (image / video / text).
                        (default: output.png)
  -b, --benchmark       Running the inference on the same input 5 times to
                        measure execution performance. (Cannot be used in
                        video mode) (default: False)
  -e ENV_ID, --env_id ENV_ID
                        A specific environment id can be specified. By
                        default, the return value of
                        ailia.get_gpu_environment_id will be used (default: 2)
  --env_list            display environment list (default: False)
  --ftype FILE_TYPE     file type list: image | video | audio (default: image)
  --debug               set default logger level to DEBUG (enable to show
                        DEBUG logs) (default: False)
  --profile             set profile mode (enable to show PROFILE logs)
                        (default: False)
  -bc BENCHMARK_COUNT, --benchmark_count BENCHMARK_COUNT
                        set iteration count of benchmark (default: 5)
```                        

Input an image file, perform AI processing, and save the output to a file.

```
python3 yolov3-tiny.py -i input.png -s output.png
```

Input an video file, perform AI processing, and save the output to a video.

```
python3 yolov3-tiny.py -v input.mp4 -s output.mp4
```

Measure the execution time of the AI model.

```
python3 yolov3-tiny.py -b
```

Run AI model on CPU instead of GPU.

```
python3 yolov3-tiny.py -e 0
```

Get a list of executable environments.

```
python3 yolov3-tiny.py --env_list
```

## Launcher

You can display a list of models and select them with the mouse by using the command below.

```
python3 launcher.py
```

## Tutorial BLOG

[ailia SDK tutorial (Python API) (EN)](https://medium.com/axinc-ai/ailia-sdk-tutorial-python-ea29ae990cf6)

[ailia SDK tutorial (Python API) (JP)](https://medium.com/axinc/ailia-sdk-%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB-python-28379dbc9649)

[ailia SDK tutorial (C++ API) (EN)](https://medium.com/axinc-ai/ailia-sdk-tutorial-c-75e59bbefffe)

[ailia SDK tutorial (C++ API) (JP)](https://medium.com/axinc/ailia-sdk-%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB-c-dc949d9dcd28)

[ailia SDK tutorial (Unity/C# API) (EN)](https://medium.com/axinc-ai/ailia-sdk-tutorial-unity-54f2a8155b8f)

[ailia SDK tutorial (Unity/C# API) (JP)](https://medium.com/axinc/ailia-sdk-%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB-unity-257fa1e98777)

[ailia SDK tutorial (JNI API) (EN)](https://medium.com/axinc-ai/ailia-sdk-tutorial-jni-92b797725e08)

[ailia SDK tutorial (JNI API) (JP)](https://medium.com/axinc/ailia-sdk-%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB-jni-7a11c1da08dc)

