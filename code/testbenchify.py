import os
import sys
import string
import re

def main():
    try:
        wd = os.getcwd()
        os.chdir(wd)
        print(wd)
        if(len(sys.argv) != 2):
            raise IOError("no file passed")
        vhdl_filename = sys.argv[1]
        project = vhdl_filename.split(".")[0]
        tb_filename = "tb_" + vhdl_filename;
        tabcount = 0;

        vhdl_file = open(vhdl_filename, 'r')
        if (os.path.isfile(tb_filename)):
            raise ValueError("tb already exists")

        #read file
        port_list = []
        generic_list = []
        port_gathering = 0
        generic_gathering = 0
        in_entity = 0
        print("processed entity: \n")
        for line in vhdl_file:
            if len(line.translate(str.maketrans('', '', string.whitespace))) > 1:
                if "entity" in line:
                    in_entity = 1;
                if in_entity == 1:
                    print(line);
                    if ( (");" in line) and not ("vector" in line) ):
                        port_gathering = 0
                        generic_gathering = 0
                    if port_gathering == 1:
                        port_list.append([line.translate(str.maketrans('', '', string.whitespace)).split(':')[0], line.translate(str.maketrans('', '', string.whitespace)).split(':')[1]]);
                    if generic_gathering == 1:
                        generic_list.append([line.translate(str.maketrans('', '', string.whitespace)).split(':')[0], line.translate(str.maketrans('', '', string.whitespace)).split(':')[1]]);
                    if "port" in line:
                        port_gathering = 1
                    if "generic" in line:
                        generic_gathering = 1
                    if "end entity" in line:
                        in_entity = 0
        regex = re.compile(r"\dto\d", re.IGNORECASE)
        for set in port_list:
            set[1] = set[1].replace(";", "", 1)
            print(set[1][0])
            if set[1][0] == "i":
                set[1] = set[1].replace("in", "", 1)
                set.append("in")
            if set[1][0] == "o":
                set[1] = set[1].replace("out", "", 1)
                set.append("out")
            set[1] = set[1].replace("downto", " downto ", 1)
            set[1] = re.sub(regex, fixport ,set[1]);

        #header/entitty
        tb_file = open(tb_filename, 'w')
        tb_file.write("library ieee;\n")
        tb_file.write("\t"* (1) + "use ieee.std_logic_1164.all;\n")
        tb_file.write("\t"* (1) + "use ieee.numeric_std.all;\n\nentity tb_" + project + " is\n")
        tb_file.write("end tb_" + project + ";\n\n")

        #architecture
        tb_file.write("architecture arch of tb_" + project + " is\n");
        tabcount = tabcount + 1
        tb_file.write("\t" * tabcount + "component " + project + " is\n");
        tabcount = tabcount + 1

        #add component
        if not (len(generic_list) == 0):
            tb_file.write("\t" * tabcount + "generic (\n");
            tabcount = tabcount + 1
            for set in generic_list:
                if not ( set == generic_list[len(generic_list)-1]):
                    tb_file.write("\t" * tabcount + set[0] + "\t:\t" + set[1] + ";\n")
                else:
                    tb_file.write("\t" * tabcount + set[0] + "\t:\t" + set[1] + "\n")
            tabcount = tabcount - 1
            tb_file.write("\t" * tabcount + ");\n");
        if not (len(port_list) == 0):
            tb_file.write("\t" * tabcount + "port (\n")
            tabcount = tabcount + 1
            for set in port_list:
                if not ( set == port_list[len(port_list)-1]):
                    tb_file.write("\t" * tabcount + set[0] + "\t:\t" + set[2] + "\t" + set[1] + ";\n")
                else:
                    tb_file.write("\t" * tabcount + set[0] + "\t:\t" + set[2] + "\t" + set[1] + "\n")
            tabcount = tabcount -1
            tb_file.write("\t" * tabcount + ");\n")

        tabcount = tabcount -1;
        tb_file.write("\t" * tabcount + "end component;\n\n")

        #generate all signals
        for set in port_list:
            tb_file.write(("\t" * tabcount + "signal s_" + set[0] + "\t:\t" + set[1] + ";\n"))
        tb_file.write("\t" * tabcount + "signal done : std_logic := '0';\n\n")

        #begin arch proper
        tabcount = 0;
        tb_file.write("begin\n");
        tabcount = tabcount + 1;

        #unit under test
        tb_file.write("\t" * tabcount + "i_" + project + " : " + project +"\n")
        tabcount = tabcount + 1
        if not (len(generic_list) == 0):
            tb_file.write("\t" * tabcount + "generic map(\n");
            tabcount = tabcount + 1
            for set in generic_list:
                if not ( set == generic_list[len(generic_list)-1]):
                    tb_file.write("\t" * tabcount + set[0] + "\t=>\t\n")
                else:
                    tb_file.write("\t" * tabcount + set[0] + "\t=>\t\n")
            tabcount = tabcount - 1
            tb_file.write("\t" * tabcount + ")\n");
        if not (len(port_list) == 0):
            tb_file.write("\t" * tabcount + "port map (\n")
            tabcount = tabcount + 1
            for set in port_list:
                if not ( set == port_list[len(port_list)-1]):
                    tb_file.write("\t" * tabcount + set[0] + "\t=>\ts_" + set[0] + ",\n")
                else:
                    tb_file.write("\t" * tabcount + set[0] + "\t=>\ts_" + set[0] + "\n")
            tabcount = tabcount -1
            tb_file.write("\t" * tabcount + ");\n\n")

        #power on
        tb_file.write("\t" * tabcount + "p_geninputs: process\n")
        tb_file.write("\t" * tabcount + "begin\n")
        tb_file.write("\t" * tabcount + "if (done = '0') then\n")
        tabcount += 1
        tb_file.write("\t" * tabcount + "done <= '1';\n")
        tb_file.write("\t" * tabcount + "s_reset_n <= '0';\n")
        tb_file.write("\t" * tabcount + "s_clock <= '1';\n")
        tb_file.write("\t" * tabcount + "wait for 10 ns;\n")
        tb_file.write("\t" * tabcount + "s_clock <= '0';\n")
        tb_file.write("\t" * tabcount + "wait for 10 ns;\n")
        tb_file.write("\t" * tabcount + "s_reset_n <= '1';\n")
        tabcount -= 1
        tb_file.write("\t" * tabcount + " end if;\n\n\n\n")

        #clock generator -- assumes a port signal called "clock"
        tb_file.write("\t" * tabcount + "s_clock <= '1';\n")
        tb_file.write("\t" * tabcount + "wait for 10 ns;\n")
        tb_file.write("\t" * tabcount + "s_clock <= '0';\n")
        tb_file.write("\t" * tabcount + "wait for 10 ns;\n")
        tabcount -= 1
        tb_file.write("\t" * tabcount + "end process;\n")
        tabcount -= 1
        tb_file.write("\t" * tabcount + "end arch;\n")
    except IOError:
        print("No file passed")
    except ValueError:
        print("tb file already persent, won't overwrite")

def fixport(arg):
    return arg.group(0).replace("to", " to ")



if __name__ == '__main__':
    main()
