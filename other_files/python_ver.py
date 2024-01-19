with open("midori_program_ver.txt", 'r') as f: 
    # Read the entire contents of the file into a string
    vernumber = f.read()

with open("model_installer.py", 'r') as f: 
    # Read the entire contents of the file into a string
    compose_yaml = f.read()

# Replace all occurrences of 'changeme ' with '["gpu"]' in the string
compose_yaml = compose_yaml.replace('changemelunaplease', f'{vernumber}')

# Write the modified string back to the file
with open("model_installer.py", 'w') as f:
    f.write(compose_yaml)

with open("localai_installer.py", 'r') as f: 
    # Read the entire contents of the file into a string
    compose_yaml = f.read()

# Replace all occurrences of 'changeme ' with '["gpu"]' in the string
compose_yaml = compose_yaml.replace('changemelunaplease', f'{vernumber}')

# Write the modified string back to the file
with open("localai_installer.py", 'w') as f:
    f.write(compose_yaml)