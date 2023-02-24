library ieee;
use ieee.std_logic_1164.all;
library work;
use work.pkg.all;


entity dct is
  port( 
            clk    : in std_logic;
	    reset_n: in std_logic;
	    wr     : in std_logic;
	    oe     : in std_logic; -- output enable
	    dct_in : in array_2d;
	    dct_out: out array_2d
       ); 
end entity;


architecture arch of dct is

	signal x : array_2d;
   
begin
	process(clk, reset_n)
	begin
		if reset_n = '0' then
			for i in 0 to BLOCK_SIZE-1 loop
				for j in 0 to BLOCK_SIZE-1 loop
					dct_out(i)(j) <= 0;
				end loop;
			end loop;
		elsif rising_edge(clk) then
			if (wr = '1') then
				x <= dct_in;
				if (oe = '1') then
					dct_out <= compute_dct(x);
				end if;
			end if;
		end if;
	end process;
		
end arch;
