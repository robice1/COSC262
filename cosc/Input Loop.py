prompt = "Enter command or 'q' for quit "
command = input(prompt)
while command != 'q':    
    print(f"You entered: {command}")
    command = input(prompt)