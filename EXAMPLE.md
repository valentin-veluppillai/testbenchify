# input file - "example.vhd"
```vhdl
library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity example is
  generic(
    n : natural
  );
  port (
    clock   : in  std_logic;    --the tool expects this to exist
    in1 : in  std_logic;
    in2    : in  std_logic_vector(n-1 downto 0);
    out1    : out  std_logic;
    out2     : out std_logic_vector(n-1 downto 0)
  );
end entity;

architecture arch of example is
  signal signal_1 : std_logic;
  signal signal_2 : std_logic_vector(0 to n-1);
begin

  p_process1 : process(clock)
  variable v1 : std_logic;
  begin
    --imagine your code here
  end process p_process1;

  p_process2 : process(clock)
  begin
    --imagine your code here
  end process p_process2;
end architecture;
```
# generated output file - "tb_example.vhd"
```vhdl
library ieee;
	use ieee.std_logic_1164.all;
	use ieee.numeric_std.all;

entity tb_example is
end tb_example;

architecture arch of tb_example is
	component example is
		generic (
			n	:	natural
		);
		port (
			clock	:	in	std_logic;
			in1	:	in	std_logic;
			in2	:	in	std_logic_vector(n-1 downto 0);
			out1	:	out	std_logic;
			out2	:	out	std_logic_vector(n-1 downto 0)
		);
	end component;

	signal s_clock	:	std_logic;
	signal s_in1	:	std_logic;
	signal s_in2	:	std_logic_vector(n-1 downto 0);
	signal s_out1	:	std_logic;
	signal s_out2	:	std_logic_vector(n-1 downto 0);
	signal done : std_logic := '0';

begin
	i_example : example
		generic map(
			n	=>		--generics cannot be generated
		)
		port map (
			clock	=>	s_clock,
			in1	=>	s_in1,
			in2	=>	s_in2,
			out1	=>	s_out1,
			out2	=>	s_out2
		);

	p_geninputs: process
	begin
		if (done = '0') then
			done <= '1';
			s_reset_n <= '0';
			wait for 20 ns;
			s_reset_n <= '1';
		end if;
	end process;

	p_genclock: process
	begin
		s_clock <= '1';
		wait for 10 ns;
		s_clock <= '0';
		wait for 10 ns;
	end process;



end arch;

```
