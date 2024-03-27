import argparse
import yaml


def main():
    print("Starting the YAML editor script...")
    parser =  argparse.ArgumentParser(description="Edit a YAML file.")
    parser.add_argument("-i", "--item", help="The item in the YAML to change.")
    parser.add_argument("-d", "--data", help="The new setting for the item.")
    parser.add_argument("file", help="The YAML file to edit.")
    args = parser.parse_args()

    print(f"The item to change is {args.item}.")
    print(f"The new setting for the item is {args.data}.")
    print(f"The YAML file to edit is {args.file}.")

    with open(args.file, "r")  as f:
        data = yaml.safe_load(f)
    
    data_type = type(data[args.item])
    print(data_type)
    print(args.data)

    with open(args.file, "r")  as f:
        data = yaml.safe_load(f)

    print(f"The current data in the YAML file is {data}.")

    # Check if the value is a string.
    try:
        print("Trying to set str")
        new_value = str(args.data)
    except ValueError:
        print(f"Error: Could not convert {args.data} to a string.")

    try:
        print("Trying to set int")
        new_value = int(args.data)
    except ValueError:
        print(f"Error: Could not convert {args.data} to an integer.")

    if args.data == "false" or args.data == "False":
        print("false to False")
        new_value = False

    if args.data == "true" or args.data == "True":
        print("true to True")
        new_value = True

    print(f"The new value is {new_value}.")

    data[args.item] = new_value

    print(f"The new data in the YAML file is {data[args.item]}.")

    with open(args.file, "w") as f:
        yaml.safe_dump(data, f)

    print("The YAML file has been edited successfully.")


if __name__ == "__main__":
    main()
