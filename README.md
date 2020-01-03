# Description
This repo is a python package for easy testing, easy deploying your model for IQTest,  visit our website: https://iqtest.pub


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
Download dataset, extract to 'data'. Or extract to customized location, and specify `DATA_ROOT` in `run_script.py`. 
config.json in dataset shows test_suites settings. 

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
When running models, uploaded datas to ftp space are readonly, only `group_data` and `train_data` are visible.   
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
├── other_datas # invisible to model
├── group_data  # shared
│   └── shared_data_example.bin
└── train_data
    └── user_train_data.bin
```

## Compress datas
Datas uploaded to ftp would be decompressed automatically.  
`tar`, `7z` would be used for decompressing.
* File contains .tar would be decompressed by `tar`
* File with `.7z,.zip,.gz,.xz,.gz2` postfix would be decompressed by `7z`

Eg.
* a.tar.gz would be decompressed by `tar`, cause `.tar` in file name
* a.gz would be decompressed by `7z`
