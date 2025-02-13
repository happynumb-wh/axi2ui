PWD 		= $(shell pwd)
AXI2UI_DIR 	= $(PWD)/axi2ui

init:
	picker export --autobuild=false osmc_axi_top.sv -w axi2ui.fst --sname osmc_axi_top --tdir $(AXI2UI_DIR) --lang python -e --sim verilator
	$(MAKE) -C $(AXI2UI_DIR) -j`nproc`
test:
	python3 $(PWD)/axi2ui.py
	
.PHONY: init test