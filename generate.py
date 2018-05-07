import sys
import numpy as np
from decimal import Decimal


def main():
    if not len(sys.argv) == 5:
        print("Usage: generate.py <template_file> <min> <max> <increment>")
        return 1

    min_enrichment = Decimal(sys.argv[2])
    max_enrichment = Decimal(sys.argv[3])
    enrichment_increment = Decimal(sys.argv[4])

    with open(sys.argv[1]) as template:
        template = template.read()
        print(min_enrichment, max_enrichment, enrichment_increment)
        for enrichment in np.arange(min_enrichment,
                max_enrichment,
                enrichment_increment):
            print(enrichment)
            generated_input = template \
                    .replace("$ENRICHMENT", str(enrichment)) \
                    .replace("$SIM_NAME", str(int(enrichment * 1000)))
            out_file_name = sys.argv[1].replace("ENRICHMENT",
                    str(int(enrichment * 1000)))
            print(out_file_name)
            out_file = open(out_file_name, 'w')
            out_file.write(generated_input)
            out_file.close()


if __name__ == "__main__":
    main()
