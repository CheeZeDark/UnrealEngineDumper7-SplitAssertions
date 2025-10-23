import os
import re

# CONFIG
folder_path = "."  # Folder with .inl files
backup = True
max_lines_per_file = 500

# REGEX
macro_start_pattern = re.compile(r'#define\s+DUMPER7_ASSERTS_\w+')
macro_end_pattern = re.compile(r'^(?!.*\\).*')  # The last line of the macro without '\'

# PROCESS FILES
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith(".inl"):
            filepath = os.path.join(root, filename)

            # Backup
            if backup:
                os.rename(filepath, filepath + ".bak")
                read_path = filepath + ".bak"
            else:
                read_path = filepath

            with open(read_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            current_chunk = []
            line_count = 0
            file_count = 1
            inside_macro = False

            for line in lines:
                stripped = line.strip()
                if macro_start_pattern.match(stripped):
                    inside_macro = True
                    macro_lines = [line]  # Adding new Macros
                elif inside_macro:
                    macro_lines.append(line)
                    if not stripped.endswith("\\"):  # Ending of Macros!!!
                        inside_macro = False
                        # Adding macros in the current chunk
                        current_chunk.extend(macro_lines)
                        line_count += len(macro_lines)
                        # Проверяем размер chunk
                        if line_count >= max_lines_per_file:
                            # Save this!!!
                            split_filename = f"{os.path.splitext(filename)[0]}_part{file_count}.inl"
                            with open(os.path.join(root, split_filename), "w", encoding="utf-8") as f_out:
                                f_out.writelines(current_chunk)
                            print(f"[+] Written {split_filename} ({line_count} lines)")
                            file_count += 1
                            current_chunk = []
                            line_count = 0
                else:
                    current_chunk.append(line)
                    line_count += 1
                    if line_count >= max_lines_per_file:
                        split_filename = f"{os.path.splitext(filename)[0]}_part{file_count}.inl"
                        with open(os.path.join(root, split_filename), "w", encoding="utf-8") as f_out:
                            f_out.writelines(current_chunk)
                        print(f"[+] Written {split_filename} ({line_count} lines)")
                        file_count += 1
                        current_chunk = []
                        line_count = 0

            # Save the remaining lines
            if current_chunk:
                split_filename = f"{os.path.splitext(filename)[0]}_part{file_count}.inl"
                with open(os.path.join(root, split_filename), "w", encoding="utf-8") as f_out:
                    f_out.writelines(current_chunk)
                print(f"[+] Written {split_filename} ({len(current_chunk)} lines)")

print("\n All .inl files processed. Macros are completed successfully!!!")

