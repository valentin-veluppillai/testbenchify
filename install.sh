mkdir /opt/testbenchify
cp ./code/testbenchify.py /opt/testbenchify/testbenchify.py
echo "#!/bin/sh\n#automatically generate vhdl testbenches form soure vhdl file\n#github.com/valentin-veluppillai/testbenchify\npython3  /opt/testbenchify/testbenchify.py" >> /bin/testbenchify
chmod a+x /bin/testbenchify
