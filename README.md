```
████████╗ ██████╗ ██╗   ██╗ ██████╗ █████╗ ███╗   ██╗███████╗████████╗██████╗ ██╗██╗  ██╗███████╗
╚══██╔══╝██╔═══██╗██║   ██║██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝
   ██║   ██║   ██║██║   ██║██║     ███████║██╔██╗ ██║███████╗   ██║   ██████╔╝██║█████╔╝ █████╗  
   ██║   ██║   ██║██║   ██║██║     ██╔══██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  
   ██║   ╚██████╔╝╚██████╔╝╚██████╗██║  ██║██║ ╚████║███████║   ██║   ██║  ██║██║██║  ██╗███████╗
   ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝     
```

A Command line tool for launching attacks against Machine Learning Malware detectors.
Based on [SecML Malware](https://github.com/zangobot/secml_malware), it provides most of the state of the art attacks directly in your shell.

## Install

```bash
conda create -n toucanstrike python=3.8
conda activate toucanstrike
pip install -r requirements.txt
```

## Usage
First, set a _target_ (it must be the name of a classifier inside the plugin folder).
We already provide these code wrappers:
* `malconv` for the [MalConv classifier](https://arxiv.org/abs/1710.09435) (along with its weights)
* `gbdt_ember` for [EMBER GBDT](https://arxiv.org/abs/1804.04637) classifier 
* `dnn_lin` and `dnn_relu` for the [DNN-Lin and DNN-ReLu](https://arxiv.org/abs/1903.04717) networks

Then, set the _data_ to use:
`data your_malware_folder`

It is time for the attack. You can type `whitebox --help` or `blackbox --help` for the list of strategies.
An example might be:
`whitebox --type partial_dos`

Finally, you can launch your test!

```
target malconv
data your_malware_folder
whitebox --type partial_dos
run
```


## Plugins
Want to add a target? Just add a folder inside the `plugin` folder! There are already some provided targets, and it is easy to learn how to make one!

## Help wanted!
If you want to include more functionalities, just open a pull request!
