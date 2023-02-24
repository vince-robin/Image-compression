library ieee;
use ieee.std_logic_1164.all;

library work;
use work.pkg.all;

entity zigzag  is
  port ( 
		 clk : in std_logic;
		 reset_n : in std_logic;
		 wr : in std_logic;
		 oe : in std_logic;
         zigzag_in : in one_block; 
		 zigzag_out: out block_flatten(0 to (BLOCK_SIZE*BLOCK_SIZE)-1)
		); 
end entity zigzag;


architecture arch of zigzag is

  signal x : one_block;
	  
begin
	process(clk, reset_n, wr, oe)
	begin
		if (reset_n = '0') then
			for i in 0 to (BLOCK_SIZE*BLOCK_SIZE)-1 loop
				zigzag_out(i) <= 0;
			end loop;
		elsif rising_edge(clk) then
			if (wr = '1') then
				x <= zigzag_in;
				if (oe = '1') then
					zigzag_out <= zig_zag(x);
				end if;
			end if;
		end if;
	end process;
	
end arch;
