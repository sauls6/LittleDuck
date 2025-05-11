import os

def parse_test_file(filepath):
    tests = {}
    current_file = None
    current_content = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                if current_file:
                    tests[current_file] = ''.join(current_content).strip()
                current_file = line[1:].strip()
                current_content = []
            else:
                current_content.append(line)
        if current_file:
            tests[current_file] = ''.join(current_content).strip()
    return tests

def write_tests_to_files(tests, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in tests.items():
        out_path = os.path.join(output_dir, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content + '\n')

if __name__ == "__main__":
    test_cases = parse_test_file('../../missing_parser_tests.txt')
    write_tests_to_files(test_cases, './tests/parser/new')
    print(f"Wrote {len(test_cases)} test files to ./tests/parser/")
