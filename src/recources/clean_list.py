if __name__ == "__main__":
    filename = input("Enter the filename: ")
    with open(filename, "r") as file:
        lines = file.readlines()
        lines = [line.strip().lower() for line in lines if line.strip() != ""]
        lines = list(set(lines))
        lines = sorted(lines)

    with open(filename, "w") as file:
        file.write("\n".join(lines))
