# TraceMeOut

Can a Neural Net learn to differentiate between user tasks by watching at the Kernel Trace? Does this accuracy defines a metric of how reverse-engineerable a system is? 🤩 


<b>How to run</b>

1️⃣ To start collecting data, run the following (Coming soon 🔜 Video tutorial on how to collect data, but it's pretty straightforward 😉)

`sudo ./collect.sh`

2️⃣To process the data, run

`./process.sh`

3️⃣ To train the neural net and check the results, run

`./trainAI.sh`


<b>Configuration</b>

The file called `configuration.py` allows the modification of the neural net's training and architecture hyperparameters. It also allows to change the size of the sliding window and sampling ratio. For more info, see "Model".

<b>Model</b>

The sampling and neural network model are as follows: in particular it requires collecting data and then processing it, as opposed to training the neural net online. It also does not support predicting over a live kernel stream, it is basically an offline experiment.

<img src="https://github.com/GastonMazzei/TraceMeOut/raw/main/utils/sampling_model.png" width=800>

<img src="https://github.com/GastonMazzei/TraceMeOut/raw/main/utils/neuralnet_model.png" width=800>

<b>Requirements</b>

- A <b>linux kernel</b> equipped with Ftrace and function_graph <i>(e.g. Ubuntu 18 and 20)</i>

- <b>Python3</b> equipped with <b>Tensorflow, NumPy</b> and <b>Pandas</b>. 

- Last but not least, the hypothesis that the kernel trace contains 'some' information from which a neural net can learn 😉

