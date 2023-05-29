# ClusterBench
ClusterBench (CBench) is a program designed to execute multiple Cosbench tests on a cluster. It simplifies the process of running benchmarks and collecting performance data in a distributed environment. This project is based on the [Cosbench](https://github.com/intel-cloud/cosbench) tool developed by Intel.

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use ClusterBench, follow these steps:

1. Clone the repository:

- If you have not installed COSBench:
     ```shell
     mkdir cosBench
     wget https://github.com/intel-cloud/cosbench/releases/download/v0.4.2.c4/0.4.2.c4.zip
     unzip 0.4.2.c4.zip
     mv 0.4.2.c4/* cosBench
     rm -r 0.4.2.c4
     rm 0.4.2.c4.zip
     cd cosBench
     git clone https://github.com/mehranasghari/ClusterBench.git
     
- If you have installed COSBench:
     

## Usage

To run ClusterBench, execute the main.sh script with the appropriate command-line arguments:
  ```shell
    ./main.sh -i input -d defaults.json -s 

## Configuration

ClusterBench requires two key components for its execution:

1. Input File: The input file provides the necessary parameters and configuration details for the Cosbench tests. Place the input file in the `input/` directory.
2. Defaults File: The defaults file contains the default settings and configurations for the tests. Modify this file as needed and place it in the `config/` directory.

