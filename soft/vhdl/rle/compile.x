echo "=> cleaning"
rm -rf work*.cf *.o

echo "=> analysis package"
echo ghdl -a --std=08 pkg.vhd
ghdl -a --std=08 pkg.vhd

echo "=> analysis design file"
echo ghdl -a --std=08 rle.vhd
ghdl -a --std=08 rle.vhd

echo "=> analysis test bench"
echo ghdl -a --std=08 rle_tb.vhd
ghdl -a --std=08 rle_tb.vhd

echo "=> elaboration"
echo ghdl -e --std=08 rle_tb
ghdl -e --std=08 rle_tb

echo "=> run"
echo ghdl -r --std=08 rle_tb
ghdl -r  --std=08 rle_tb --wave=rle_tb.ghw

echo "=> result analysis"
gtkwave rle_tb.ghw rle_tb.sav
