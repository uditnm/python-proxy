def load_blocklist():
    blocklist =  set()
    try:
        with open("blocklist.txt", "r") as file:
            for line in file:
                if not line:
                    continue

                hostname = line.split()[1]
                blocklist.add(hostname)
    except FileNotFoundError:
        print(f"Warning: file not found. Running with an empty blocklist.")
        
    return blocklist