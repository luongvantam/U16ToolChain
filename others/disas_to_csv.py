import re
import csv
import sys


def convert_txt_to_csv(input_file, output_file):
    pattern = re.compile(
        r"^\d:([0-9A-F]+)H\s+[0-9A-F]+\s+(.+)$",
        re.IGNORECASE
    )

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in, \
         open(output_file, "w", newline="", encoding="utf-8") as f_out:

        writer = csv.writer(
            f_out,
            quoting=csv.QUOTE_ALL
        )

        writer.writerow(["address", "instruction"])

        for line in f_in:
            line = line.strip()

            if line.endswith(":"):
                continue

            match = pattern.match(line)
            if not match:
                continue

            address = match.group(1).upper().zfill(5)
            instruction = match.group(2).strip().lower()

            writer.writerow([address, instruction])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python disas_to_csv.py input.txt output.csv")
        sys.exit(1)

    convert_txt_to_csv(sys.argv[1], sys.argv[2])
