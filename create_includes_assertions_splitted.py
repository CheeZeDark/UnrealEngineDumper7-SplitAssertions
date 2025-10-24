import os

# === CONFIGURATION ===
input_folder = "."       # Files for .inl :D
output_file = os.path.join(input_folder, "Assertions_All.inl")

inl_files = [f for f in os.listdir(input_folder) if f.endswith(".inl")]
inl_files.sort()

with open(output_file, "w", encoding="utf-8") as out_f:
    out_f.write("// === Auto-generated Assertions_All.inl ===\n")
    out_f.write("#pragma once\n\n")
    for filename in inl_files:
        out_f.write(f'#include "{filename}"\n')

print(f" Main include created: {output_file}")
