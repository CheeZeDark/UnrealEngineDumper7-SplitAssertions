import os

# === CONFIGURATION ===
input_file = "Assertions.inl"        # your big .inl file
lines_per_chunk = 1000               # how many lines per chunk
output_prefix = "Assertions_part"    # name prefix for parts
combined_file = "Assertions_all.inl" # final include file name
encoding = "utf-8"

# === READ INPUT FILE ===
with open(input_file, "r", encoding=encoding) as f:
    lines = f.readlines()

total = len(lines)
chunks = (total + lines_per_chunk - 1) // lines_per_chunk

print(f"Splitting {input_file} ({total} lines) into {chunks} parts...")

# === CREATE CHUNK FILES ===
part_files = []
for i in range(chunks):
    start = i * lines_per_chunk
    end = min((i + 1) * lines_per_chunk, total)
    part_filename = f"{output_prefix}{i + 1}.inl"
    part_files.append(part_filename)

    with open(part_filename, "w", encoding=encoding) as out:
        out.writelines(lines[start:end])

    print(f"  → Created {part_filename} ({end - start} lines)")

# === CREATE MASTER INCLUDE FILE ===
with open(combined_file, "w", encoding=encoding) as f:
    f.write("// Auto-generated include file\n")
    f.write("// This file includes all Assertion parts in order.\n\n")
    for part in part_files:
        f.write(f'#include "{part}"\n')

print(f"\n✅ Done! Created {combined_file} with {chunks} includes.")
print("\nNow replace your old include line with:\n")
print(f'#include "{combined_file}"')