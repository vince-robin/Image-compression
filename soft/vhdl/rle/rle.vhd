library ieee;
use ieee.std_logic_1164.all;

library work;
use work.pkg.all;


entity rle is
  port( 
		   clk : in std_logic;
		   reset_n : in std_logic;
		   wr : in std_logic;
		   oe : in std_logic;
		   rle_in : in block_flatten(0 to (IN_LENGTH-1)); 
		   rle_out: out block_flatten(0 to (2*IN_LENGTH-1)) -- dans le pire des cas, longueur = 128
	 ); 
end entity;


architecture arch of rle is

  signal x : block_flatten(0 to (IN_LENGTH-1));
	  
begin
	process(clk, reset_n, wr, oe)
	begin
		if (reset_n = '0') then
			for i in 0 to 2*IN_LENGTH-1 loop
				rle_out(i) <= 0;
			end loop;
		elsif rising_edge(clk) then
			if (wr = '1') then
				x <= rle_in;
				if (oe = '1') then
					rle_out <= run_length_encode(x);
				end if;
			end if;
		end if;
	end process;
	
end arch;
