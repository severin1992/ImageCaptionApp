# Image Caption Web App
Based on [1][2] I developed an image caption generator web app build with the [dash framework](https://plot.ly/products/dash/) in Python. Just drag and drop or select a picture and the Web App takes care of the rest. 
For a more complete documentation of our model architecture feel free to visit our [blog post](https://humboldt-wi.github.io/blog/research/seminar/07imagecaptioning/).


---
![plain](captionwebapp1.png)

---
![filled](captionwebapp2.png)

---
Instructions: <br>
I can recommend to install Anaconda and create a virtual environment for trying out the web app. You must have Keras (2.0 or higher) installed with either the TensorFlow or Theano backend. You also need scikit-learn, Pandas, NumPy, and Matplotlib. <br>
Furthermore, you will need to install the dash packages: 
pip install dash==0.19.0  # The core dash backend
pip install dash-renderer==0.11.1  # The dash front-end
pip install dash-html-components==0.8.0  # HTML components
pip install dash-core-components==0.16.0  # Supercharged components
pip install plotly==2.2.3  # Plotly graphing library used in examples

Here are some tipps for [package management with anaconda](https://conda.io/docs/user-guide/tasks/manage-pkgs.html#viewing-a-list-of-installed-packages). In the *InstalledPackages.txt* file you can find all the packages I have had installed for the project. 

Clone the github repository to a local folder and activate your virtual environment (source activate *yourENVname*). Navigate with the terminal to your folder and enter 'python app.py'. Now visit '''http:127.0.0.1:8050/''' in your web browser.

---
Sources: <br>
[1] Jason Brownlee. How to Develop a Deep Learning Photo Caption Generator from Scratch, November 2017.
[2] Marc Tanti, Albert Gatt, and Kenneth P. Camilleri. Where to put the Image in an Image Caption Generator. arXiv preprint arXiv:1703.09137, 2017.
