# ClusterBench
ClusterBench (CBench) is a program designed to execute multiple Cosbench tests on a swift cluster (Open Stack Swift). It simplifies the process of running benchmarks and collecting performance data in a distributed environment. This project is based on the [Cosbench](https://github.com/intel-cloud/cosbench) tool developed by Intel.

## Table of Contents

- [Installation](#Installation)
- [Configuration](#configuration)
- [Usage](#Usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To Install ClusterBench, follow these steps:

- If you have not installed COSBench:

  1. Install openjdk-8-jre
     ```shell
     sudo apt install openjdk-8-jre
     ```

  2. Clone the repositories:

       ```shell
       mkdir cosBench
       wget https://github.com/intel-cloud/cosbench/releases/download/v0.4.2.c4/0.4.2.c4.zip
       unzip 0.4.2.c4.zip
       mv 0.4.2.c4 cosBench
       rm 0.4.2.c4.zip
       cd cosBench
       wget https://github.com/mehranasghari/ClusterBench/archive/refs/heads/main.zip
      ```


  3. Run COSBench
    ```shell
     chmod +x *.sh
     ./start-all.sh &
     ```
    web interface is available on http://localhost:19088/controller/index.html
 
- If you have installed COSBench:
     

## Configuration

ClusterBench components:

1. Benchmark File: Benchmark file provides the necessary parameters and configuration details for the Cosbench tests. You can change the benchmark file in `/conf/benchmark.cfg` path based on your need. Furthermore you can create your own bnechmark file and pass that file into the command line as an argument with `-b` or `--benchmark-file` switch

2. Defaults File: The defaults file contains the default settings and configurations for the tests and benchmarks. Modify this file as needed and place it in the `conf/defaults.json` path. You can also make your custome defaults file and pass it by `-d` or `--default-file` switch when you are running a benchmark.

3. Script File: Script file is a Bash file that execute before every workload that sent to cluster. You can find it at `/app/pre_test_script.sh` path. Further you can pass your own script file with `-s` or `--script-file` switch.


## Usage

To run ClusterBench, execute the send_load.sh script.
You can also use the appropriate command-line arguments:

  ```shell
    ./send_load.sh  or
    ./send_load.sh -b benchmark-file -d defaults-file -s script-file
  ```




