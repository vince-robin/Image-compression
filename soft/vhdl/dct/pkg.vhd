library ieee;
use ieee.std_logic_1164.all;

package pkg is

    constant Q_LEVEL    : integer := 50; -- niveau de quantification
    constant BLOCK_SIZE : integer := 8;
    
    type  array_1d is array (0 to BLOCK_SIZE-1) of integer;
    type  array_2d is array (0 to BLOCK_SIZE-1) of array_1d;
    
    function compute_mat_mul(mat1: array_2d; mat2:array_2d) return array_2d;
    function compute_dct(input_of_dct: array_2d) return array_2d;
    

	-- *100 par rapport à la DCT de base (avec arrondi à l'unité),
	-- dans le but de ne plus avoir de nombres flottants.
	constant  DCT_MATRIX : array_2d  := (
		( 35,  35,  35,  35,  35,  35,  35,  35 ),
		( 49,  42,  28,  10, -10, -28, -42, -49 ),
		( 46,  19, -19, -46, -46, -19,  19,  46 ),
		( 42, -10, -49, -28,  28,  49,  10, -42 ),
		( 35, -35, -35,  35,  35, -35, -35,  35 ),
		( 28, -49,  10,  42, -42, -10,  49, -28 ),
		( 19, -46,  46, -19, -19,  46, -46,  19 ),
		( 10, -28,  42, -49,  49, -42,  28, -10 )
	);
	
	-- matrice de la norme JPEG (pour la luminance)
	constant  Q : array_2d := (
		( 16, 11, 10, 16,  24,  40,  51,  61 ),
		( 12, 12, 14, 19,  26,  58,  60,  55 ),
		( 14, 13, 16, 24,  40,  57,  69,  56 ),
		( 14, 17, 22, 29,  51,  87,  80,  62 ),
		( 18, 22, 37, 56,  68, 109, 103,  77 ),
		( 24, 35, 55, 64,  81, 104, 113,  92 ),
		( 49, 64, 78, 87, 103, 121, 120, 101 ),
		( 72, 92, 95, 98, 112, 100, 103,  99 )
	);
	
	-- matrice sur laquelle on va appliquer la DCT
	constant ORIGINAL_BLOCK : array_2d := (
		( 154, 123, 123, 123, 123, 123, 123, 136 ),
		( 192, 180, 136, 154, 154, 154, 136, 110 ),
		( 254, 198, 154, 154, 180, 154, 123, 123 ),
		( 239, 180, 136, 180, 180, 166, 123, 123 ),
		( 180, 154, 136, 167, 166, 149, 136, 136 ),
		( 128, 136, 123, 136, 154, 180, 198, 154 ),
		( 123, 105, 110, 149, 136, 136, 180, 166 ),
		( 110, 136, 123, 123, 123, 136, 154, 136 )
	); 
	
    
end pkg;

package body pkg is


	-- effectue la multiplication de deux matrices
	function compute_mat_mul(mat1: array_2d; mat2:array_2d) return array_2d is
		
		variable output: array_2d;
		variable elem: integer;
	  
		begin
			for i in 0 to 7 loop
				for j in 0 to 7 loop
					elem := 0;
					for k in 0 to 7 loop
						elem := elem + mat1(i)(k)*mat2(k)(j);
					end loop;
					output(i)(j) := elem;
				end loop;
			end loop;
		return output;
	end compute_mat_mul;

	-- calcule la DCT-2D
	function compute_dct(input_of_dct: array_2d) return array_2d is
		
		variable t_matrix_transpose : array_2d;
		variable m_matrix : array_2d;
		variable d_matrix : array_2d;
		variable q_matrix : array_2d;
		variable c_matrix : array_2d;
		variable temp     : array_2d;
		variable output   : array_2d;
	  
		begin
			for i in 0 to BLOCK_SIZE-1 loop
				for j in 0 to BLOCK_SIZE-1 loop
					 m_matrix(i)(j) := input_of_dct(i)(j) - 128;
					 t_matrix_transpose(i)(j) := DCT_MATRIX(j)(i);
				end loop;
			end loop;
			
			temp := compute_mat_mul(DCT_MATRIX, m_matrix);
			d_matrix := compute_mat_mul(temp, t_matrix_transpose);
			   
			for i in 0 to BLOCK_SIZE-1 loop 
				for j in 0 to BLOCK_SIZE-1 loop
					if (Q_LEVEL < 50) then
						q_matrix(i)(j) := (50/Q_LEVEL)*Q(i)(j);
					end if;
					if (Q_LEVEL > 50) then
						q_matrix(i)(j) := ((100-Q_LEVEL)/50)*Q(i)(j);
					end if;
					if (Q_LEVEL = 50) then
						q_matrix(i)(j) := Q(i)(j);
					end if;
					if (q_matrix(i)(j) > 255) then
						q_matrix(i)(j) := 255;
					end if;
					-- division par 10000 car on a multiplié les coefficients de la DCT par 100
					-- et on a effectué la multiplication de la matrice des coefficients DCT 
					-- par sa transposée à la ligne 97/98 (donc 100*100 = 10000)
					c_matrix(i)(j) := (d_matrix(i)(j))/(q_matrix(i)(j))/10000; 
				end loop;
			end loop;
			output := c_matrix;
		return output;
	end compute_dct;

end package body;
