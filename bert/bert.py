import time
import os
import urllib.request

import numpy as np

import ailia


weight_path = "bert-base-uncased.onnx"
model_path = "bert-base-uncased.onnx.prototxt"

rmt_ckpt = "https://storage.googleapis.com/ailia-models/bert_en/"

if not os.path.exists(model_path):
    urllib.request.urlretrieve(rmt_ckpt + model_path, model_path)
if not os.path.exists(weight_path):
    urllib.request.urlretrieve(rmt_ckpt + weight_path, weight_path)


# load dataset
dummy_input = np.ones((1, 128))

# net initialize
env_id = ailia.get_gpu_environment_id()
print(env_id)
net = ailia.Net(model_path, weight_path, env_id=env_id)

# compute time
for i in range(10):
    start = int(round(time.time() * 1000))
    preds_ailia = net.predict((dummy_input, dummy_input, dummy_input))[0]
    end = int(round(time.time() * 1000))
    print("ailia processing time {} ms".format(end-start))

print(f'[DEBUG] output shape: {preds_ailia.shape}')
print('Successfully finished!')
