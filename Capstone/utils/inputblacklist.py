def sanitize_input(password, username):
    black_list =["'",";","--","-","SELECT","DROP","DELETE","UPDATE","ALTER","INSERT","TRUNCATE","JOIN", "REPLACE", "<SCRIPT>", "<", ">"]
    for black_list_item in black_list:
        if black_list_item.lower() in username.lower() or black_list_item.lower() in password.lower():
            raise ValueError("black list error")