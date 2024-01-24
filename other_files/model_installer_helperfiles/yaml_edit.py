import yaml
import argparse

parser = argparse.ArgumentParser(description='Edit YAML file.')
parser.add_argument('-i', '--item', help='Item to change.')
parser.add_argument('-d', '--data', help='New data for the item.')
parser.add_argument('yaml_file ', help='YAML file to edit.')

args = parser.parse_args()

# Open the YAML file
with open(args.yaml_file, 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

# Check if the item exists in the data
if args.item not in data:
    print(f"Error: Item '{args.item}' not found in YAML file.")
    exit(1)

# Edit the data
data[args.item] = args.data

# Resave the YAML file
with open(args.yaml_file, 'w') as f:
    yaml.dump(data, f)

print(f"Successfully updated '{args.item}' with '{args.data}' in {args.yaml_file}.")
