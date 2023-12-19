#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
print(sys.argv)
prog_name = sys.argv.pop(0)
input_file_name = sys.argv.pop(0) if sys.argv else '/home/gill/tmp/mexico_music.txt'
td_cells = [f"(h.td % '{line.strip()}')" for line in open(input_file_name, 'r') ]
n_rows = len(td_cells) // 2
#print(td_cells)
rows = [f"h.tr % ({td_cells[i_row*2]} + {td_cells[1+i_row*2]}) +" for i_row in range(n_rows)]
row_list = '\n'.join(rows)
table = f"h.table % ({row_list})"
print(table)
output_file_name = os.path.splitext(input_file_name)[0] + '.phileas'
with open(output_file_name, 'w') as output:
    output.write(table)
