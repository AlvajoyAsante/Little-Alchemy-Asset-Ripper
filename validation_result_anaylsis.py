import os


if __name__ == "__main__": 
    validation_results_file = "validation/validation_results.txt"
    validation_results = []
    not_in_validation = []
    image_folder = "ELEMENTS/RAW"

    # read all files in the raw folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]
    image_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    
    print("This is meant to be used after the validation analysis has been completed.")
    print("This will remove files that were not detected by the validation analysis.")

    response = input("Do you want to continue? (y/n): ")

    # check if the validation file exists
    if not os.path.exists(validation_results_file):
        print("Validation results file does not exist.")
        exit(1)

    if response == "y" or response == "Y":
        # read the validation results
        with open(validation_results_file, 'r') as file:
            for line in file.readlines():
                name, image_file = line.strip().split(', ')
                validation_results.append(image_file)

        # check which files were not detected by the validation analysis
        for name in image_files:
            if name not in validation_results:
                not_in_validation.append(name)

        if not_in_validation:
            # print the files that were not detected by the validation analysis
            print("A total of", len(not_in_validation), "files were not detected by the validation analysis.")
            print("The following files were not detected by the validation analysis:")
            for name in not_in_validation:
                print(name)

            # ask the user if they want to remove the files
            result = input("Do you want to remove these files? (y/n): ")
            if result == "y" or result == "Y":
                for name in not_in_validation:
                    # move the files to the doc folder                    
                    os.remove(os.path.join(image_folder, name))

                    # remove them from the list
                    image_files.remove(name)

                print("Files removed.")

                # rename the files starting from 1
                file_number = 1
                for name in image_files:
                    os.rename(os.path.join(image_folder, name), os.path.join(image_folder, f"{file_number}.png"))
                    file_number += 1

            else:
                print("Files were not removed.")
        else:
            print("All files were detected by the validation analysis.")

       
        print("Processing complete.")