import json

with open("output/output.json", 'r') as f:
    generated_data = json.load(f)

with open("asm_json/acm_out_IE_starhub_010825.json", 'r') as f:
    reference_data = json.load(f)

# --- Key comparison ---
generated_keys = set(generated_data.keys())
reference_keys = set(reference_data.keys())

print("--- Key Comparison ---")
print(f"Generated keys count: {len(generated_keys)}")
print(f"Reference keys count: {len(reference_keys)}")
missing_in_generated = reference_keys - generated_keys
if missing_in_generated:
    print(f"Keys in reference but not in generated: {missing_in_generated}")
extra_in_generated = generated_keys - reference_keys
if extra_in_generated:
    print(f"Keys in generated but not in reference: {extra_in_generated}")

# --- Channel comparison ---
print("\n--- Channel Comparison ---")
generated_channels = generated_data.get('channels', [])
reference_channels = reference_data.get('channels', [])
print(f"Generated channels count: {len(generated_channels)}")
print(f"Reference channels count: {len(reference_channels)}")

generated_channel_ids = {c['id'] for c in generated_channels if 'id' in c}
reference_channel_ids = set()
for i, c in enumerate(reference_channels):
    if 'id' in c:
        reference_channel_ids.add(c['id'])
    else:
        print(f"Reference channel at index {i} has no 'id' key.")

missing_channels = reference_channel_ids - generated_channel_ids
if missing_channels:
    print(f"Channels in reference but not in generated ({len(missing_channels)}): {sorted(list(missing_channels))}")

extra_channels = generated_channel_ids - reference_channel_ids
if extra_channels:
    print(f"Channels in generated but not in reference ({len(extra_channels)}): {sorted(list(extra_channels))}")

common_ids = generated_channel_ids.intersection(reference_channel_ids)
if common_ids:
    channel_id_to_compare = sorted(list(common_ids))[0]
    print(f"\nComparing first common channel: {channel_id_to_compare}")

    gen_channel = next(c for c in generated_channels if c.get('id') == channel_id_to_compare)
    ref_channel = next(c for c in reference_channels if c.get('id') == channel_id_to_compare)

    if gen_channel == ref_channel:
        print("Channel objects are identical.")
    else:
        print("Channel objects are different.")
        # For a detailed diff, we would need a proper library.
        # For now, just printing them is a good start.
        # print("\n--- Generated Channel ---")
        # print(json.dumps(gen_channel, indent=2, sort_keys=True))
        # print("\n--- Reference Channel ---")
        # print(json.dumps(ref_channel, indent=2, sort_keys=True))
else:
    if len(generated_channels) > 0:
        print("No common channel IDs found to compare. Showing first generated channel.")
        print(json.dumps(generated_channels[0], indent=2, sort_keys=True))
    else:
        print("No channels in generated file to compare.")
