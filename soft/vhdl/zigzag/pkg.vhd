library ieee;
use ieee.std_logic_1164.all;

package pkg is

	constant BLOCK_SIZE: natural := 8; 
	
    type array_1D	     is array (0 to BLOCK_SIZE-1) of integer;
    type one_block       is array (0 to BLOCK_SIZE-1) of array_1D;
    type block_flatten   is array (integer range <>) of integer;
    
    function zig_zag (img : one_block) return block_flatten;

    
end package;


package body pkg is

	function zig_zag (img : one_block) return block_flatten is

		variable h : integer := 0;
		variable v : integer := 0;
		variable i : integer;

		variable hmin : integer := 0;
		variable vmin : integer := 0;

		variable hmax : integer := block_size;
		variable vmax : integer := block_size;

		variable output : block_flatten(0 to (hmax*vmax)-1):=(others=> 0);
		
		begin
			  i := 0;
			  while ((v<vmax) and (h<hmax)) loop
			  
				if(((h+v) mod 2)= 0) then
				
					if(v=vmin) then
						output(i) := img(v)(h);
						if(h = hmax) then
							v:=v+1;
						else
							h:=h+1;
						end if;
						i:=i+1;
						
					elsif((h = hmax-1) and (v<vmax)) then
						output(i) := img(v)(h);
						v:=v+1;
						i:=i+1;
					
					elsif((v>vmin) and (h< hmax-1)) then
						output(i) := img(v)(h);
						v:=v-1;
						h:=h+1;
						i:=i+1;
					end if;
					
				else 
				
					if((v = vmax-1) and (h<= hmax-1)) then
						output(i) := img(v)(h);
						h:=h+1;
						i:=i+1;
						
					elsif(h = hmin) then
						output(i) := img(v)(h);
						if(v= vmax-1) then
							h:=h+1;
						else
							v:=v+1;
						end if;
						i:=i+1;
					
					elsif((v<vmax-1) and (h>hmin)) then
						output(i) := img(v)(h);
						v:=v+1;
						h:=h-1;
						i:=i+1;						
					end if;
				end if;
			  
			  if((v=vmax-1) and (h=hmax-1)) then
				output(i) := img(v)(h);
				exit;
			  end if;
			  
			end loop;
		return output;
	end zig_zag;
		
end package body;
