import os

# Set to current working directory (safe fallback for __file__)
BASE_DIR = os.getcwd()

INCLUDE_EXTENSIONS = (
    '.php', '.module', '.inc', '.install', '.yml', '.yaml',
    '.twig', '.js', '.ts', '.css', '.scss', '.md'
)

MAX_FILE_SIZE_MB = 1.0  # Warn if file exceeds this size

def get_all_files(root_path):
    file_list = []
    for dirpath, _, filenames in os.walk(root_path):
        for file in filenames:
            if file.endswith(INCLUDE_EXTENSIONS):
                full_path = os.path.join(dirpath, file)
                file_list.append(full_path)
    return file_list

def dump_module(module_path, module_name):
    output_file = os.path.join(BASE_DIR, f"{module_name}_dump.txt")
    files = get_all_files(module_path)

    with open(output_file, 'w', encoding='utf-8') as out:
        for file_path in files:
            rel_path = os.path.relpath(file_path, BASE_DIR)
            out.write(f"\n\n===== FILE: {rel_path} =====\n\n")
            try:
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    out.write(f"[Warning: File is {file_size_mb:.2f} MB — may be too large for AI parsing]\n\n")
                with open(file_path, 'r', encoding='utf-8') as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"[Error reading file: {e}]\n")

        # Add summary footer
        out.write("\n\n===== SUMMARY =====\n")
        out.write(f"Module: {module_name}\n")
        out.write(f"Files Dumped: {len(files)}\n")
        ext_list = sorted(set(os.path.splitext(f)[1] for f in files))
        out.write("Includes: " + ", ".join(ext_list) + "\n")
        out.write("Ready for: AI Analysis ✅\n")

    print(f"✅ Dumped: {module_name} → {output_file}")

def main():
    for name in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, name)
        if os.path.isdir(full_path):
            info_file = os.path.join(full_path, f"{name}.info.yml")
            if os.path.exists(info_file):
                dump_module(full_path, name)

if __name__ == "__main__":
    main()
