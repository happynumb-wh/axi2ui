
.PHYONY: all

all:
	picker export --autobuild=false osmc_axi_top.sv -w axi2ui.fst --sname osmc_axi_top --tdir picker_out_adder/ --lang python -e --sim verilator