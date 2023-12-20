import hashlib
def main():
    while True:
        dict_hashes={}
        msg1 = input ('Type exit at anytime to end program...')
        if msg1.lower() == 'exit':
            break
        else:
            msg2 = input('Enter mode (add|login):')
            if msg2.lower() == 'add':
                username = input("Please enter a username ")
                password = input("Please enter your password ")
                hash_user = hashlib.sha256(username.encode())
                hash_password = hashlib.sha256(password.encode())
                dict_hashes[hash_user.hexdigest()] = [hash_password.hexdigest()]

            elif msg2.lower()=='login':
                    username1 = input("Please enter a username ")
                    password1 = input("Please enter your password ")
                    hash_user1 = hashlib.sha256(username1.encode())
                    hash_password1 = hashlib.sha256(password1.encode())
                    if hash_user1 in dict_hashes:
                        if hash_password1 == dict_hashes[hash_user1]:
                         print("Login successful.")
                        else:
                         print("Incorrect password.")
                    else: print("Incorrect username")

if __name__ == '__main__':
    main()