# testbenchify
Generate vhdl testbenches form source vhdl files!
## Usage
This tool generates tb_file.vhd form file.vhd. The tool assumes the existence of a port named 'clock', where it automatically generates a 50MHz clock signal.
```sh  
testbenchify input-file  
```
## Installation
This tool requires [Python 3](https://www.python.org/) to work.
```sh
sudo apt install python3 -y
git clone https://github.com/valentin-veluppillai/testbenchify
cd testbenchify/scripts
sudo ./install.sh
```
## Uninstallation
```sh
cd /path/to/repo/testbenchify
sudo scripts/uninstall.sh
```
