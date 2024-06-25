# offline-eth-wallet/generate_wallet.py

from eth_account import Account
#from mnemonic import Mnemonic
from eth_utils import to_checksum_address
#import secrets
import getpass

def create_account(passphrase: str = "", num_words: int = 12, language: str = "english"):
    Account.enable_unaudited_hdwallet_features()
    account, mnemonic_phrase = Account.create_with_mnemonic(passphrase=passphrase, num_words=num_words, language=language)
    return account, mnemonic_phrase

def verify_mnemonic(mnemonic_phrase: str, passphrase: str, account) -> bool:
    derived_account = Account.from_mnemonic(mnemonic_phrase, passphrase=passphrase)
    return derived_account.address == account.address

def verify_private_key(private_key: str, public_address: str) -> bool:
    derived_account = Account.from_key(private_key)
    derived_address = to_checksum_address(derived_account.address)
    return derived_address == public_address

def save_wallet_to_file(filename: str, mnemonic_phrase: str, passphrase: str, private_key: str, public_address: str):
    with open(filename, "w") as f:
        f.write(f"Mnemonic Phrase: {mnemonic_phrase}\n")
        f.write(f"Passphrase: {passphrase}\n")
        f.write(f"Private Key: {private_key}\n")
        f.write(f"Public Address: {public_address}\n")

def get_secure_passphrase() -> str:
    while True:
        passphrase = getpass.getpass("Enter a passphrase (optional, press Enter to skip): ")
        if passphrase:
            passphrase_verify = getpass.getpass("Re-enter the passphrase for verification: ")
            if passphrase == passphrase_verify:
                return passphrase
            else:
                print("Passphrases do not match. Please try again.")
        else:
            return passphrase

def generate_secure_paper_wallet():
    # Get user inputs
    passphrase = get_secure_passphrase()
    num_words = int(input("Enter the number of words desired for your mnemonic phrase. Must be [12, 15, 18, 21, 24]"))

    # Generate mnemonic and account
    account, mnemonic_phrase = create_account(passphrase=passphrase, num_words=num_words)

    # Get the private key in hexadecimal format
    private_key = account.key.hex()
    public_address = to_checksum_address(account.address)

    # Verify mnemonic and private key
    mnemonic_check = verify_mnemonic(mnemonic_phrase, passphrase, account)
    private_key_check = verify_private_key(private_key, public_address)

    print(f"Mnemonic Phrase: {mnemonic_phrase}")
    print(f"Private Key: {private_key}")
    print(f"Public Address: {public_address}")
    print(f"Validate account can be recovered from mnemonic... {mnemonic_check}")
    print(f"Validate private key corresponds to public address... {private_key_check}")

    # Save the details to a file securely
    save_wallet_to_file("paper_wallet.txt", mnemonic_phrase, passphrase, private_key, public_address)
    print("Paper wallet generated and saved to paper_wallet.txt.")

if __name__ == "__main__":
    generate_secure_paper_wallet()
