from stix2 import Indicator
from stix2validator import validate_file, validate_instance, print_results, validate_string

indicator = Indicator(name="File hash for malware variant",
                      pattern="[file:hashes.md5 = 'd41d8cd98f00b204e9800998ecf8427e']",
                      pattern_type="stix")
print(indicator.serialize(pretty=True))

results = validate_string(indicator.serialize(pretty=True))
print_results(results)