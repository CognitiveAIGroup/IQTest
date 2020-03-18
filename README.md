# Description
This repo is a python package for easy testing, easy deploying your model for IQTest,  visit our website: https://iqtest.pub

# Event
## Call For Participants: IJCAI-2020 Machine Automated IQ Test Challenge
### Introduction  
As one of the predominant benchmarks for measuring human intelligence, Intelligence Quotient (IQ) test provides a natural and excellent AI benchmark for testing the current development of AI research. For better solving IQ tests automatedly by machines, one needs to use, combine and advance many areas in AI including knowledge representation and reasoning, machine learning, natural language processing and image understanding.  

The IJCAI-2020 Machine Automated IQ Test Challenge (MAIQ’2020) contains three categories including verbal comprehension, diagram reasoning and sequence reasoning, all questions are collected from genuine IQ Test questions for human being. By given a SDK and some dataset, participants are required to develop programs to solve these problems automatically.

Finalists are invited to attend IJCAI’2020 for the on-site competition, on which the final ranking will be made and announced. Also, finalists are strongly encouraged to open their source codes as well as to submit a paper describing how their systems work.

### Participation
The competition is open to all groups. Individuals could form a group, and register a shared team account on the website. After validation using a team email, any group could attend the competition. The champion and the runner-up teams are requested either to open their source code or to submit a system paper. 

For help please contact us: 

| | |
| ---- | ---- |
| Organizer: | yzhou@bsbii.cn |
| Technical support: | hbwang@bsbii.cn |

### Instruction for competition 
1. Register as team on the website: https://iqtest.pub
2. Finish your model using sdk & data provided by this repo
3. Upload your model and data

Please visit our website for more details: https://iqtest.pub 

# How to install
```
pip install .
```

# How to use
## Example
* in entry.json specify entry python file
* in entry python file 
    * provide get_eval_cls 
    >    ```python
    >    def get_eval_cls(category: str) -> object:
    >        pass
    >    ```
    * or provide get_model_object
    >    ```python
    >   def get_model_object(category: str) -> object:
    >       pass
    >    ```
    now there are three categories, return `None` would ignore the corresponding competition 
    check example for more details
    * provide global_pre_run (optional)
    >    ```python
    >   def global_pre_run():
    >       pass
    >    ```
    Used for global setup, such as setup environment, load  train data so etc.
* in example/run_script.py, client_mode, server_mode, pack_model provided 

# Test data
## Clone from Github
Dataset locates under data
## Download from Website
Download dataset, extract to 'data'. Or extract to customized location, and specify `DATA_ROOT` in `run_script.py`. 
config.json in dataset shows test_suites settings. 
## Version history
Current Version 0.2.4
```
    "0.1": "update data_file_name.json for test caseupdate data_file_name.answer.json for answers",
    "0.2": "add verbal1-public.json case",
    "0.2.1.1": "add T1-105-public.json case",
    "0.2.1.2": "fix T1-105-public.json case",
    "0.2.2": "update data",
    "0.2.3": "update some data",
    "0.2.4": "add more train data, fix inconsistency"
```

# How to use data
## TL;TR
* upload/rename compressed file would trigger decompressing
* upload private data to ftp://host/train_data
* upload shared data to ftp://host/group_data (Group members cannot upload/list/delete group_data, but could use it)
  * _join/create a group to share data_

## Space for Train Data
Please signup our website as a team for more information.

## Space for Group share Data
If your team joins a group, group_data would be shared between group members.   
The directory name is `group_data`, and maps to ftp://api.iqtest.pub:9001/group_data   
**Notation!**, Cause ftp service `chroot jail`, group members have no priviledge to list/upload/delete group_data.

## Directory structures
When running models, data uploaded to ftp space are readonly, only `group_data` and `train_data` are visible.   
Check `run_model_with_pre_traindata` example.  
We recommend use the same directory strucures with provided example.  
Note: `train_data` would be prepended automatically.
```
.
├── your_script_with_train_data 
│   ├── entry.json
│   ├── eval_with_traindata.py
│   ├── other_dirs
│   │   ├── scripts_A.py
│   │   ├── ... 
│   │   ...
│   │   └── so etc. 
|   |   ...
│   ├── so etc.
│   └── run_script.py
├── group_data
│   └── shared_data_example.bin
└── train_data
    └── user_train_data.bin
```

Directories in ftp
```
.
├── other_data # invisible to model
├── group_data  # shared
│   └── shared_data_example.bin
└── train_data
    └── user_train_data.bin
```

## Compress data
Data uploaded to ftp would be decompressed automatically.  
`tar`, `7z` would be used for decompressing.
* File contains .tar would be decompressed by `tar`
* File with `.7z,.zip,.gz,.xz,.gz2` postfix would be decompressed by `7z`

Eg.
* a.tar.gz would be decompressed by `tar`, cause `.tar` in file name
* a.gz would be decompressed by `7z`
