PWD 			= $(shell pwd)
SRC_DIR 		= $(PWD)/src
AXI2UI_DIR 		= $(SRC_DIR)/axi2ui
RTL_DIR 		= $(PWD)/rtl
WAIVER_DIR 		= $(PWD)/src
TRACE_DIR 		= $(PWD)/test/data
# TRACE_FILE 		= $(TRACE_DIR)/trace/cactusADM_0_rand100w.txt
TRACE_FILE      = $(TRACE_DIR)/astar_biglake_1085_trace.txt.simple.drank
INTERNAL_FILE 	= $(PWD)/internal.yaml
SPLIT_MODULE	= split_osmc_axi_top
TOP_MODULE 		= osmc_axi_top
PYTEST_THREADS = 4

DUT_SO_PATH 	= $(AXI2UI_DIR)/_UT_$(TOP_MODULE).so
LIBPYTHON_PATH	= $(shell python -c "import sysconfig; print(sysconfig.get_config_var('LIBPL') + '/' + sysconfig.get_config_var('LDLIBRARY'))")
LD_PRELOAD_ADD	=$(DUT_SO_PATH):$(LIBPYTHON_PATH)

VCS_VFLAG	:= '-kdb' \
			'-timescale=1ns/1ps' \
			'-diag' 'timescale' \
			'+notimingcheck'\
			'+nospecify' \
			'+lint=TFIPC-L' \
			'-diag=sdf:verbose' \
			'+plusarg_save' '-debug_access+pp+dmptf+thread' \
			'-debug_region=cell+encrypt' '-notice' \
			'+define+RANDOMIZE_REG_INIT'  \
			'-cm' 'line+cond+fsm+tgl' \
			'-cm_hier' '$(PWD)/axi2ui_cm_hier.cfg' \
			'-cm_name' 'simv' \
			'-cm_dir'  '$(PWD)/cov' \
		    '-f' '$(RTL_DIR)/axi2ui_filelist.f'

init-verilator:
	picker export --autobuild=false $(RTL_DIR)/$(TOP_MODULE).sv -w $(PWD)/axi2ui.fst --sname $(TOP_MODULE) --tdir $(AXI2UI_DIR) --lang python -e -c --sim verilator --internal $(INTERNAL_FILE)
	$(MAKE) -C $(AXI2UI_DIR)

init-vcs:
	picker export --autobuild=false $(RTL_DIR)/$(SPLIT_MODULE)/$(TOP_MODULE).sv -V '"$(VCS_VFLAG)"' -F 600MHz -w $(PWD)/axi2ui.fsdb --sname $(TOP_MODULE) --tdir $(AXI2UI_DIR) --lang python -e -c --sim vcs --internal $(INTERNAL_FILE)
	python modify.py
	$(MAKE) -C $(AXI2UI_DIR)

run:
	LD_PRELOAD=$(LD_PRELOAD):$(LD_PRELOAD_ADD) python3 $(SRC_DIR)/main.py $(TRACE_FILE)
run-debug:
	LD_PRELOAD=$(LD_PRELOAD):$(LD_PRELOAD_ADD) python3 -m pdb $(SRC_DIR)/main.py $(TRACE_FILE)

test:
	LD_PRELOAD=$(LD_PRELOAD):$(LD_PRELOAD_ADD) pytest --toffee-report -sv $(SRC_DIR) -W ignore::DeprecationWarning

# vcs查看波形
verdi:
	verdi -ssf $(PWD)/axi2ui.fsdb -sswr $(PWD)/signal.rc

# vcs查看覆盖率报告
cov:
	verdi -cov -covdir $(PWD)/cov.vdb

clean:
	rm -rf $(AXI2UI_DIR)
	
.PHONY: init test