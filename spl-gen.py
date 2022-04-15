import os
import re
import subprocess


class User:
    """class to get infos of the user who wants to create a token."""
    def __init__(self, network=None, quantity=None, keypair=None, public_key=None):
        self.network = network
        self.quantity = quantity
        self.keypair = keypair
        self.public_key = public_key
        self.keypair = keypair

    def get_network(self):
        while True:
            res = input("On which network do you want to create a token ?\n1) Mainnet\n2) Devnet\n").lower()
            if res == "1" or res == "mainnet":
                self.network = "mainnet-beta"
                print(f"You picked {self.network}. Real money !")
                break
            elif res == "2" or res == "devnet":
                self.network = "devnet"
                print(f"You picked {self.network}.")
                break
            else:
                print("Invalid input.")

    def get_quantity(self):
        while True:
            try:
                self.quantity = int(input("\nHow many tokens do you want to mint ? \n"))
                break
            except ValueError:
                print("Invalid number. Try again ...")

    def get_pubkey(self):
        while True:
            res = input("What is your public key ? (Solana address)\n")
            if re.match(r"[A-Za-z0-9]{43,44}", res):
                self.public_key = str(res)
                break
            else:
                print("Wrong format. Try again ...")

    # def get_keypair(self):
    #     with os.scandir(os.getcwd()) as folder:
    #         for file in folder:
    #             if file.name.endswith(".json") and file.is_file():
    #                 if "key" in file.name.lower():
    #                     self.keypair = file.name
    #                     print('---' * 37)
    #                     print(f"Successfully found key.json file.")
    #                     print('---' * 37)
    #     if not self.keypair:
    #         print('Could not retrieve your private key file.\nPlease put it in the same directory as the script'
    #               ' and make sure you name it "key.json".')
    #         exit()

    def get_keypair(self):
      """Getting the keypair either by the path or automatically"""
        while True:
            res = input("Please enter the PATH of your private key file.\n")
            try:
                with open(str(res), 'r') as keyfile:
                    keyfile.read()
                    self.keypair = str(res)
                    log.write(f"Private key file found at {self.keypair}\n")
                    break
            except FileNotFoundError:
                print("File not found, try again.")
            except Exception as err:
                print(err)

    def get_all(self):
        self.get_keypair()
        self.get_network()
        self.get_quantity()
        self.get_pubkey()


class Token:
    """Class to create a token with the network, the number of tokens to mint, a
            private key path and a public key !"""
    def __init__(self, address=None, token_account=None, token_mint=None):
        self.address = address
        self.token_account = token_account
        self.token_mint = token_mint

    def create_token(self):
        try:
            log.write(f"User picked {user.network}.\n\n")
            cmd = f"spl-token create-token --url {user.network} --fee-payer " \
                  f"{user.keypair} --mint-authority {user.public_key}"
            result = subprocess.check_output(cmd, shell=True, universal_newlines=True)

            log.write(result)

            if "Signature:" in result:
                self.address = result[15:59]

                print(f"Token successfully created !")
                log.write("Token successfully created !\n\n")

        except Exception as err:
            print(f"An error occured during token creation. Please check requisites and try again.\n"
                  f"{err}")
            log.write(str(err))

    def create_token_account(self):
        try:
            account_cmd = f"spl-token create-account --url {user.network} --fee-payer {user.keypair} " \
                                       f"--owner {user.public_key} {token.address}"
            account_result = subprocess.check_output(account_cmd, shell=True, universal_newlines=True)
            if "Signature:" in account_result:
                self.token_account = account_result[17:61]
                print(f"Token account created at {self.token_account}")
                log.write(f"Token account created at {self.token_account}\n\n")
        except Exception as err:
            print(f"An error occured during token creation. Please check requisites and try again.\n"
                  f"{err}")

    def mint(self):
        mint_cmd = f"spl-token mint --url {user.network} --fee-payer {user.keypair} --mint-authority " \
                   f"{user.keypair} {self.address} {user.quantity} {self.token_account}"

        mint_result = subprocess.check_output(mint_cmd, shell=True, universal_newlines=True)
        if "Signature:" in mint_result:

            print(f"{user.quantity} tokens were successfully minted!")
            log.write(f"Tokens successfully minted!\n\n{mint_result}")
            log.write(f"https://solscan.io/token/{self.address}?cluster=devnet")

            print(f"\nCheck your token at https://solscan.io/token/{self.address}?cluster=devnet")

    def initialize(self):
        self.create_token()
        self.create_token_account()
        self.mint()


if __name__ == '__main__':

    # CREATING A LOG FILE.
    log = open('logs.txt', 'w', encoding='utf8')

    # GETTING ALL USER INFOS
    user = User()
    user.get_all()

    # CREATING TOKEN
    token = Token()
    token.initialize()

    # SAVING LOGS
    log.close()
