PWD 		= $(shell pwd)
AXI2UI_DIR 	= $(PWD)/axi2ui
TRACE_DIR 	= $(PWD)/test/data
TRACE_FILE 	= $(TRACE_DIR)/cactusADM_0_rand100w.txt

init:
	picker export --autobuild=false osmc_axi_top.sv -w axi2ui.fst --sname osmc_axi_top --tdir $(AXI2UI_DIR) --lang python -e -c --sim verilator
	$(MAKE) -C $(AXI2UI_DIR) -j`nproc`
test:
	python3 $(PWD)/axi2ui.py $(TRACE_FILE)
	gtkwave axi2ui.fst
.PHONY: init test