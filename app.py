import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import base64
import json
import pandas as pd
import plotly
import io
import cStringIO
import re

from pickle import load
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model
from IPython.display import display
from PIL import Image


app = dash.Dash()

app.scripts.config.serve_locally = True

app.layout = html.Div([
	html.H1(children='Image Caption Web App'),

	html.Div(children='''
	This is our image caption web application. Just drop your file below and a caption will be generated.
'''),
	html.Div(id='waitfor'),
	dcc.Upload(
		id='upload',
		children=html.Div([
			'Drag and Drop or ',
			html.A('Select an Image')
		]),
		style={
			'width': '90%',
			'height': '60px',
			'lineHeight': '60px',
			'borderWidth': '1px',
			'borderStyle': 'dashed',
			'borderRadius': '5px',
			'textAlign': 'center',
			'margin': '10px'
		}
	),
	html.Div(id='output'),
])



@app.callback(Output('output', 'children'),
			  [Input('upload', 'contents')])

def update_output(contents):
	if contents is not None:
		content_type, content_string = contents.split(',')
		if 'image' in content_type:
			return html.Div([
				html.Img(src=contents, style = {'max-width': '500px'}),
				html.Hr(),
				html.Div('Image Caption: ' + generate_caption(contents), style ={'font-size': '20px'}),
			])
# extract features from each photo in the directory
def extract_features(file):
	# load the model
	model = VGG16()
	# re-structure the model
	model.layers.pop()
	model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
	# load the photo
	#image = load_img(filename, target_size=(224, 224))
	# convert base64 image into PIL image format
	file = re.sub('data:image/.+base64,','',file).decode('base64')
	file = Image.open(cStringIO.StringIO(file))
	#resize image becaus keras expects standardized input data
	file = file.resize((224,224))
	#convert the image pixels to a numpy array
	image = img_to_array(file)
	# reshape data for the model
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	# prepare the image for the VGG model
	image = preprocess_input(image)
	# get features
	feature = model.predict(image, verbose=0)
	return feature


# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

# generate a description for an image
def generate_desc(model, tokenizer, photo, max_length):
	# seed the generation process
	in_text = 'startseq'
	# iterate over the whole length of the sequence
	for i in range(max_length):
		# integer encode input sequence
		sequence = tokenizer.texts_to_sequences([in_text])[0]
		# pad input
		sequence = pad_sequences([sequence], maxlen=max_length)
		# predict next word
		yhat = model.predict([photo,sequence], verbose=0)
		# convert probability to integer
		yhat = argmax(yhat)
		# map integer to word
		word = word_for_id(yhat, tokenizer)
		# stop if we cannot map the word
		if word is None:
			break
		# append as input for generating the next word
		in_text += ' ' + word
		# stop if we predict the end of the sequence
		if word == 'endseq':
			break
	return in_text


def generate_caption(xz):
	# load the tokenizer
	tokenizer = load(open('tokenizer2.pkl', 'rb'))
	# pre-define the max sequence length (from training)
	max_length = 34
	# load the model
	model = load_model('model-ep003-loss3.608-val_loss3.858.h5')
	# load and prepare the photograph
	photo = extract_features(xz)
	# generate description
	description = generate_desc(model, tokenizer, photo, max_length)
    # delete 'startseq' at the beginning
	description_cleaned1=description.replace('startseq','')
    # delete 'endseq' at the end
	description_cleaned2=description_cleaned1.replace('endseq','')
    # capitalize first word of sentence (not working right now)
	description_cleaned3=description_cleaned2[:1].upper() + description_cleaned2[1:]
	return description_cleaned3


app.css.append_css({
	"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
	app.run_server(debug=True)
