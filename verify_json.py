import json

def compare_json_files(file1, file2):
    with open(file1, 'r') as f1:
        data1 = json.load(f1)
    with open(file2, 'r') as f2:
        data2 = json.load(f2)

    # Sort lists before comparing
    sort_lists(data1)
    sort_lists(data2)

    if data1 == data2:
        print("JSON files are identical.")
    else:
        print("JSON files are different.")
        # You can add more detailed comparison logic here if needed.

def sort_lists(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            sort_lists(value)
    elif isinstance(obj, list):
        # Sort lists of dictionaries by a common key if possible
        # This is a bit tricky since the sorting key might not always be 'id'
        # For this specific case, we know the keys, so we can hardcode them.
        if all(isinstance(i, dict) and 'id' in i for i in obj):
            obj.sort(key=lambda x: x['id'])

        for item in obj:
            sort_lists(item)

if __name__ == "__main__":
    compare_json_files("output/output.json", "asm_json/acm_out_IE_starhub_010825.json")
