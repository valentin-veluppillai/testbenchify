library ieee;
	use ieee.std_logic_1164.all;
	use ieee.numeric_std.all;

entity tb_install is
end tb_install;

architecture arch of tb_install is
	component install is
	end component;

	signal done : std_logic := '0';

begin
	i_install : install
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
