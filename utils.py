import json

def save_variables_in_text_file(list_of_variabes, save_path):
    
    # Save to a single text file
    output_file = "variables.json"
    with open(output_file, "w") as file:
        json.dump(data_to_save, file, indent=4)

    print(f"Variables saved to {output_file}")

