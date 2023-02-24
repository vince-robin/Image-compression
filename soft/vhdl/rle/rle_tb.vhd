--------------------------------------------------------------------------------
-- this file was generated automatically by Vertigo Ruby utility
-- date : (d/m/y h:m) 09/02/2023 21:02
-- author : Vincent Robin
--------------------------------------------------------------------------------
 
library ieee;
use ieee.std_logic_1164.all;

library std;
use std.textio.all;

library work;
use work.pkg.all;


entity rle_tb is
end entity;

architecture bhv of rle_tb is
  --------------------------------------------------------------------------------
  -- constants and signals 
  --------------------------------------------------------------------------------
  constant HALF_PERIOD : time :=5 ns;

  signal rle_in  : block_flatten(0 to (IN_LENGTH-1));
  signal rle_out : block_flatten(0 to (2*IN_LENGTH-1));
  
  signal clk : std_logic := '0'; 
  signal running : boolean := true;
  signal reset_n : std_logic := '0';
  signal oe : std_logic := '0';
  signal wr : std_logic := '0';
  
  --------------------------------------------------------------------------------
  -- procedure 
  --------------------------------------------------------------------------------
  procedure wait_cycles(n : natural) is 
  begin
    for i in 0 to n-1 loop
      wait until rising_edge(clk);
    end loop;
  end procedure;

begin
  --------------------------------------------------------------------------------
  -- Reset and clock 
  --------------------------------------------------------------------------------
	reset_n <= '0','1' after 123 ns;
	
	clk <= not(clk) after HALF_PERIOD when running else clk;
  --------------------------------------------------------------------------------
  -- Design Under Test (DUT)
  --------------------------------------------------------------------------------
  dut : entity work.rle(arch)
    port map (
      clk        => clk       ,
      reset_n    => reset_n   ,
	  wr         => wr        ,
      oe         => oe        ,
      rle_in  => rle_in       ,
      rle_out => rle_out   
    );
  --------------------------------------------------------------------------------
  -- sequential stimuli
  --------------------------------------------------------------------------------
  stim : process 
  
    file     IN_FILE: text;
	variable IN_LINE: line;
    variable IN_STATUS: file_open_status;

    variable input_block: block_flatten(0 to (IN_LENGTH-1)); 
 
  begin
    report "running testbench for zigzag_tb(arch)"; 
	oe <= '0';
	wr <= '0';
	
	for i in 0 to (IN_LENGTH-1) loop 
		rle_in(i) <= 0;
	end loop;
	
	report "waiting for asynchronous reset";
	wait until reset_n = '1';
	wait_cycles(10);
	
    file_open(IN_STATUS, IN_FILE, "stim.txt", read_mode);
	while not endfile(IN_FILE) loop 
		for i in 0 to IN_LENGTH - 1 loop
			readline(IN_FILE, IN_LINE);
			read(IN_LINE,input_block(i));
		end loop;
	end loop;
    file_close(IN_FILE);
		
	wr <= '1';		
	rle_in <= input_block; 	
	wait_cycles(1);  
	oe <= '1';
    wait_cycles(10);  
    report "end of simulation";
	running <= false;
	wait;
  end process;

end bhv;
