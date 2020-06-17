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
| Technical support: | pbhu@bsbii.cn |

### Instruction for competition 
1. Register as team on the website: https://iqtest.pub
2. Download dataset, finish your model
3. Upload your answer file for test cases 

Please visit our website for more details: https://iqtest.pub 

# How to use
* unzip data/datas-version.tar.gz
    * train data end with public.json, the answers end with public.answer.json postfile
    * test data end with private.json postfix
    * public.config.json/private.config.json specifies the data's categories
* Using your mode to solve test data, and output the answer to according files
> EG. answer file for seq-private.json should be named as seq-private.answer.json
> ```
> {
>    "1": {"answer":[3]},
>    "2": {"answer":[2]},
>    ...
>    so etc
>}
>```
* put all answer files under one directory, compress the directory then upload.
    * using 7z compress directory as .7z, or tar compress directory as .tar.gz are recommended

## Compress data
Data uploaded to ftp would be decompressed automatically.  
`tar`, `7z` would be used for decompressing.
* File contains .tar would be decompressed by `tar`
* File with `.7z,.zip,.gz,.xz,.gz2` postfix would be decompressed by `7z`
> a.tar.gz would be decompressed by `tar`, cause `.tar` in file name
> a.gz would be decompressed by `7z`
