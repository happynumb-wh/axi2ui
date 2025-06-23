#!/bin/python3
import re
import sys
import os

# TODO: 当编译rtl打开split选项时, filelist.f需注释掉$(PWD)/src/axi2ui/osmc_axi_top.sv, 启用split_filelist_path相关逻辑
#       当编译rtl关闭split选项时, 不启用split_filelist_path相关逻辑

# 获取脚本所在的当前目录
script_dir = os.path.dirname(os.path.abspath(__file__))
filelist_path = os.path.join(script_dir, "filelist.f")
split_dir = os.path.join(script_dir, "rtl/split_osmc_axi_top")
split_filelist_path = os.path.join(split_dir, "filelist.f")
output_dir = os.path.join(script_dir, "rtl")
output_path = os.path.join(output_dir, "axi2ui_filelist.f")

if __name__ == "__main__":

    # 确保 ./rtl 目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取文件并替换 $(PWD) 为当前目录的绝对路径
    try:
        with open(filelist_path, "r") as infile, open(output_path, "w") as outfile, \
             open(split_filelist_path, "r") as infile_split:

            content = infile.read().replace("$(PWD)", script_dir)

            # 写入到目标文件
            outfile.write(content)
        
            # 添加split files到目标文件
            outfile.write('\n\n')
            for line in infile_split:
                newline = split_dir + "/" + line
                outfile.write(newline)

        print(f"change save to : {output_path}")

    except FileNotFoundError as e:
        print(f"Error: filelist.f or not found: {e}")
    except Exception as e:
        print(f"Error: {e}")
        
    print("complete")
