import re

def read_and_sort_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    messages = [msg.strip() for msg in content.split('@@') if msg.strip()]
    return {extract_seme(msg): msg for msg in sorted(messages, key=extract_seme)}

def extract_seme(message):
    match = re.search(r':20C::SEME//([^\s\r\n]+)', message)
    return match.group(1) if match else ''

def compare_messages(file1_msgs, file2_msgs):
    all_keys = set(file1_msgs.keys()).union(set(file2_msgs.keys()))
    results = []

    for seme in sorted(all_keys):
        msg1 = file1_msgs.get(seme)
        msg2 = file2_msgs.get(seme)

        if msg1 and msg2:
            if msg1 != msg2:
                # Compare tag lines only
                diffs = get_differences_by_tag(msg1, msg2)
                if diffs:
                    results.append(f"DIFFERENCE in SEME: {seme}")
                    results.extend(diffs)
                    results.append("-" * 80)
        elif msg1:
            results.append(f"Only in File1: SEME {seme}")
        elif msg2:
            results.append(f"Only in File2: SEME {seme}")
    
    return results

def get_differences_by_tag(msg1, msg2):
    lines1 = [line.strip() for line in msg1.splitlines() if line.strip().startswith(':')]
    lines2 = [line.strip() for line in msg2.splitlines() if line.strip().startswith(':')]

    tag_map1 = {get_tag_key(line): line for line in lines1}
    tag_map2 = {get_tag_key(line): line for line in lines2}

    all_tags = set(tag_map1.keys()).union(tag_map2.keys())
    differences = []

    for tag in sorted(all_tags):
        val1 = tag_map1.get(tag)
        val2 = tag_map2.get(tag)
        if val1 != val2:
            differences.append(f"Tag {tag} differs:")
            if val1:
                differences.append(f"  File1: {val1}")
            if val2:
                differences.append(f"  File2: {val2}")
    
    return differences

def get_tag_key(line):
    # Extracts something like :20C: or :32A: as the tag key
    match = re.match(r'^(:\d{2}[A-Z]?:)', line)
    return match.group(1) if match else line

# File paths
file1 = r"C:\path\to\your\file1.txt"
file2 = r"C:\path\to\your\file2.txt"

# Process and compare
file1_msgs = read_and_sort_messages(file1)
file2_msgs = read_and_sort_messages(file2)
comparison = compare_messages(file1_msgs, file2_msgs)

# Output results
output_file = r"C:\path\to\your\comparison_result.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(comparison))

print("Comparison complete. Results saved to:", output_file)
