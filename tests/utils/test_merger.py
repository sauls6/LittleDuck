import os

def merge_tests_from_folder(input_dir, output_file):
    test_files = sorted(os.listdir(input_dir))
    with open(output_file, 'w', encoding='utf-8') as out:
        for filename in test_files:
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().rstrip()
                out.write(f'# {filename}\n{content}\n\n')

if __name__ == "__main__":
    input_dir = '../lexer'
    output_file = '../lexer_tests.txt'
    merge_tests_from_folder(input_dir, output_file)
    print(f"Merged tests written to {output_file}")
