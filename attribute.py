# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.gridspec as gridspec
import numpy as np
import tensorflow.compat.v1 as tf
print("[+] Imported Tensorflow.")
from bricklink_api.auth import oauth
print("[+] Imported OAuth from BrickLink API.")
from bricklink_api.catalog_item import get_price_guide, Type, NewOrUsed
print("[+] Imported Price Fetch Module from BrickLink API..")
import json
print("[+] Imported JSON...")
import os

#import tensorflow as tf
tf.compat.v1.disable_eager_execution()

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.compat.v1.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


if __name__ == "__main__":
  file_name = "tensorflow/examples/label_image/data/grace_hopper.jpg"
  model_file = \
    "tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb"
  label_file = "tensorflow/examples/label_image/data/imagenet_slim_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255
  input_layer = "input"
  output_layer = "InceptionV3/Predictions/Reshape_1"

  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed")
  parser.add_argument("--graph", help="graph/model to be executed")
  parser.add_argument("--labels", help="name of file containing labels")
  parser.add_argument("--input_height", type=int, help="input height")
  parser.add_argument("--input_width", type=int, help="input width")
  parser.add_argument("--input_mean", type=int, help="input mean")
  parser.add_argument("--input_std", type=int, help="input std")
  parser.add_argument("--input_layer", help="name of input layer")
  parser.add_argument("--output_layer", help="name of output layer")
  args = parser.parse_args()

  if args.graph:
    model_file = args.graph
  if args.image:
    file_name = args.image
  if args.labels:
    label_file = args.labels
  if args.input_height:
    input_height = args.input_height
  if args.input_width:
    input_width = args.input_width
  if args.input_mean:
    input_mean = args.input_mean
  if args.input_std:
    input_std = args.input_std
  if args.input_layer:
    input_layer = args.input_layer
  if args.output_layer:
    output_layer = args.output_layer

  graph = load_graph(model_file)
  t = read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.compat.v1.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)

########### Define OAuth Creds from External File ###########
######## READ EXTERNAL DATA ##########
  #open the externally saved and defined credentials file for readings
  data = open("bricklink_api/auth.json", "r")
  authData = data.read()
  creds = json.loads(authData)
  #fetch credential data from dictionary
  consumer_key = creds['ConsumerKey']
  consumer_secret = creds['ConsumerSecret']
  token_value = creds['TokenValue']
  token_secret = creds['TokenSecret']
  auth = oauth(consumer_key, consumer_secret, token_value, token_secret) 

############ Begin Finding Final Guess and Calculating Confidence ##############
  #top_k is the list of itemized lego part numbers, in order by best guess
  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)
  confidence = int(max(results)*100)
  finalGuess = labels[top_k[0]]
  print("Piece ID: "+str(finalGuess))
  print("Confidence: "+str(confidence)+"%")
  # json_obj will carry the dictionary of information we will fetch from Bricklink
  json_obj = get_price_guide("PART", finalGuess, new_or_used=NewOrUsed.USED, auth=auth)
  # we can iterate through nested dictionaries to get the data we actually want
  avg_price = json_obj.get('data').get('avg_price')
 # Let's just print this value to make sure it's right and for troubleshooting
  print("Six Month Average Selling Price: $",avg_price)
  # use our final guess to hunt down the corresponding contrast image. 
  contrast = Image.open('ContrastImages/'+finalGuess+'.PNG')
  compare = Image.open(file_name)
  contrastiar = np.array(contrast)
  # Create 2x2 sub plots
  gs = gridspec.GridSpec(2, 2)

  fig = plt.figure()
  ax1 = fig.add_subplot(gs[0, 0]) # row 0, col 0

  ax2 = fig.add_subplot(gs[0, 1]) # row 0, col 1

  ax3 = fig.add_subplot(gs[1, :]) # row 1, span all columns

  # show the contrast image in the top left
  ax1.imshow(contrastiar)
  # show the originally submitted image in top right
  ax2.imshow(compare)
  #ax3.imshow()
  ax1.axis('off')
  ax2.axis('off')
  ax3.axis('off')

  xloc = plt.MaxNLocator(12)
  ax2.xaxis.set_major_locator(xloc)
  #display our final quesses 
  plt.text(0, 0.8, 'Piece ID: '+finalGuess, dict(size=30))
  plt.text(0, 0.4, 'Confidence: '+str(confidence)+'%', dict(size=30))
  plt.text(0, 0, 'Average Cost: $'+str(avg_price), dict(size=30))
  plt.show()
