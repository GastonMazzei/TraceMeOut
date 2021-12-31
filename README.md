# TraceMeOut

<b>Can a Neural Net learn to differentiate between user tasks by watching at the Kernel Trace? Does this accuracy defines a metric of how reverse-engineerable a system is?</b> 🤩 


<b>How to run</b>

1️⃣ To start collecting data, run the following (Coming soon 🔜 Video tutorial on how to collect data, but it's pretty straightforward 😉)

`sudo ./collect.sh`

2️⃣To process the data, run the following. 

`./process.sh`

<i>Profiling yields that +90% of the time is spent at `build_data` and `parser` in `pythonscripts/Processor3.py`, so an algorithm in C/FORTRAN to convert yamls to adjacency lists is a great way to contribute :-)</i>


3️⃣ To train the neural net and check the results, run

`./trainAI.sh`

But it's quite more comfortable to take advantage of GoogleColab's GPU by using 

`./utils/TraceMeOut_4GoogleColab.ipynb`


<b>Configuration</b>

The file called `configuration.py` allows the modification of the neural net's training and architecture hyperparameters. It also allows to change the size of the sliding window and sampling ratio. The equivalent of the `configuration.py` file if training in Colab is a Jupyter Netbook cell. For more info about what each parameter means, see "Model".

<b>Model</b>

The sampling and neural network model are as follows: in particular it requires collecting data and then processing it, as opposed to training the neural net online. It also does not support predicting over a live kernel stream, it is basically an offline experiment.

<img src="https://github.com/GastonMazzei/TraceMeOut/raw/main/utils/sampling_model.png" width=800>

<img src="https://github.com/GastonMazzei/TraceMeOut/raw/main/utils/neuralnet_model.png" width=800>

<b>Results</b> 🔨👷<i>Next task: improve the net's performance</i>

What follows are results for the simple case of the binary classification task defined by listening to music on YouTube Vs having the video paused. The database for that is composed by the trace of 4 CPU cores, currently part of the repo in the directory `processed_trace`. There are 20-30 secs. of trace data sampled at 100 microseconds, which have led to ~5Mb databases per core. If using Google Colab, which is recommended as it carries the "latest" version, the data is automatically curled as part of the code. The latest results so far are the following ones 😃


<img src="https://github.com/GastonMazzei/TraceMeOut/raw/main/utils/latest_reported_performance.png" width=800>

<b> Neural Network Architecture </b>


<img src="https://github.com/GastonMazzei/TraceMeOut/raw/main/utils/neuralnet_architecture.png" width=800>


<b>Tree Encoding</b>

<img src="https://github.com/GastonMazzei/TraceMeOut/raw/main/utils/tree_encoding.png" width=800>

<b>Requirements</b>

- A <b>linux kernel</b> equipped with Ftrace and function_graph <i>(e.g. Ubuntu 18 and 20)</i>

- <b>Python3</b> equipped with <b>Tensorflow</b>(+2.5)<b>, NumPy</b> and <b>Pandas</b>. 

- Last but not least, the hypothesis that the kernel trace contains 'some' information from which a neural net can learn 😉

