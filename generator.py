import requests
import json
import re

# The official Unicode 17.0 emoji test file
UNICODE_URL = "https://www.unicode.org/Public/17.0.0/emoji/emoji-test.txt"


def generate_emoji_json():
    print(f"Fetching latest emoji data from {UNICODE_URL}...")
    response = requests.get(UNICODE_URL)

    if response.status_code != 200:
        print("Error: Could not retrieve the Unicode file.")
        return

    emoji_data = []
    current_group = ""
    current_subgroup = ""

    # Regular expression to parse lines like:
    # 1F600 ; fully-qualified # 😀 E1.0 grinning face
    emoji_line_re = re.compile(
        r"^([0-9A-F ]+)\s+;\s+([a-z-]+)\s+#\s+(\S+)\s+E\d+\.\d+\s+(.+)$"
    )

    for line in response.text.splitlines():
        line = line.strip()

        # Update categories
        if line.startswith("# group:"):
            current_group = line.replace("# group:", "").strip()
            continue
        if line.startswith("# subgroup:"):
            current_subgroup = line.replace("# subgroup:", "").strip()
            continue

        # Parse emoji data lines
        match = emoji_line_re.match(line)
        if match:
            codepoints_raw, status, char, name = match.groups()

            # We typically want "fully-qualified" emojis for a standard list
            # But we'll include all to be comprehensive as requested
            emoji_entry = {
                "emoji": char,
                "name": name,
                "codepoints": codepoints_raw.strip(),
                "status": status,
                "group": current_group,
                "subgroup": current_subgroup,
            }
            emoji_data.append(emoji_entry)

    # Save to JSON
    output_file = "unicode_17_emojis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(emoji_data, f, ensure_ascii=False, indent=4)

    print(f"Success! Generated {len(emoji_data)} emoji entries in '{output_file}'.")


if __name__ == "__main__":
    generate_emoji_json()
