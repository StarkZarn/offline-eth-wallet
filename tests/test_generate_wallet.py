# test_generate_wallet.py

from pathlib import Path
import pytest
import sys
from eth_account import Account
from eth_utils import is_checksum_address

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from generate_wallet import create_account, verify_mnemonic, verify_private_key, save_wallet_to_file

# Test parameters
num_words_cases = [12, 15, 18, 21, 24]
passphrases = ["", "Test ing-1@234`!"]

@pytest.mark.parametrize("num_words", num_words_cases)
@pytest.mark.parametrize("passphrase", passphrases)
def test_create_account(num_words, passphrase):
    account, mnemonic_phrase = create_account(passphrase=passphrase, num_words=num_words)
    
    # Check types
    assert isinstance(account.address, str)
    assert isinstance(account.key, bytes)
    assert isinstance(mnemonic_phrase, str)

    # Check private key length and content
    private_key = account.key.hex()
    assert len(private_key) == 64
    assert all(c in '0123456789abcdef' for c in private_key)

    # Verify mnemonic and private key
    assert verify_mnemonic(mnemonic_phrase, passphrase, account)
    assert verify_private_key(private_key, account.address)

def test_save_wallet_to_file(tmp_path):
    filename = tmp_path / "test_wallet.txt"
    account, mnemonic_phrase = create_account()
    private_key = account.key.hex()
    public_address = account.address

    save_wallet_to_file(filename, mnemonic_phrase, "", private_key, public_address)

    with open(filename) as f:
        lines = f.readlines()
    
    assert "Mnemonic Phrase: " in lines[0]
    assert mnemonic_phrase in lines[0]
    assert "Passphrase: " in lines[1]
    assert "Private Key: " in lines[2]
    assert private_key in lines[2]
    assert "Public Address: " in lines[3]
    assert is_checksum_address(lines[3].split()[-1])

if __name__ == "__main__":
    pytest.main()
