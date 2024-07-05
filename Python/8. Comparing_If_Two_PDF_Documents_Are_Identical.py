import hashlib

def hash_file(filename1, filename2):
    h1 = hashlib.sha1()
    h2 = hashlib.sha1()

    try:
        with open(filename1, "rb") as file:
            chunk = file.read(1024)
            while chunk:
                h1.update(chunk)
                chunk = file.read(1024)

        with open(filename2, "rb") as file:
            chunk = file.read(1024)
            while chunk:
                h2.update(chunk)
                chunk = file.read(1024)

        return h1.hexdigest(), h2.hexdigest()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None
    except Exception as e:
        print(f"An error occured: {e}")
        return None, None
    

# File Location:
file1 = r"C:\Users\hp5cd\Desktop\Projects\pd1.pdf"
file2 = r"C:\Users\hp5cd\Desktop\Projects\pd2.pdf"

msg1, msg2 = hash_file(file1, file2)
if msg1 and msg2:
    if msg1 != msg2:
        print("These files are not identical.")
    else:
        print("These files are identical.")
else:
    print("One or both files are not readable")