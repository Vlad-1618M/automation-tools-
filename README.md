**Process Monitoring Tool:**

***
This is a Python script that measures the CPU usage, memory usage, and disk usage of a running process on a system. It also outputs the results to either the terminal or a file.
***

>Dependencies:  
The following dependencies are required to run this script
>* psutil
>* datetime
>* argparse
>* colorama


You can install them via pip:

 ``` pip install psutil datetime argparse colorama ```  

***  
<B> 

**Usage**:

``` usage: monitor_process.py [-h] process_name [--output-type {terminal,file}]

Measure CPU, Memory and Disk usage for a given process.

positional arguments:
  process_name          Name of the process to monitor.

optional arguments:
  -h, --help            show this help message and exit
  --output-type {terminal,file}
                        Output to either terminal or file. Default is terminal.
```
>Example usage to monitor a process named python and output to a file:  
```python monitor_process.py python --output-type file```

  
