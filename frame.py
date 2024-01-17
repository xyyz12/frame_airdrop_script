from web3 import Web3,HTTPProvider
from eth_account.messages import encode_defunct
import requests

#获取钱包签名
def get_signature(from_address, private_key):
    
    from_address = from_address.lower()
    
    message = f"Hi, I am {from_address} and I want to claim my airdrop!"
    
    encoded_message = encode_defunct(text=message)
    signed_message = Web3().eth.account.sign_message(encoded_message, private_key=private_key)
    signature = signed_message.signature.hex()
    
    return signature


#查询空投信息
def get_airdrop_info(from_address,signature):

    from_address = Web3.toChecksumAddress(from_address)

    headers = {
        'authority': 'claim.frame-api.xyz',
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://www.frame.xyz',
        'referer': 'https://www.frame.xyz/',
        'user-agent': 'Mozilla/5.0',
    }

    json_data = {
        'signature': signature,
        'address': from_address,
    }

    try:
        response = requests.post('https://claim.frame-api.xyz/authenticate', headers=headers, json=json_data).json()
        amount = response['userInfo']['totalAllocation']
        volume = response['userInfo']['volumeTraded']
        rank = response['userInfo']['rank']
        
        return amount,volume,rank
    except Exception as e:
        print(e)
        return 0,0,0  
        
        
if __name__ == '__main__':
    
    # #钱包地址
    # from_address = '0x5E'
    
    # #钱包私钥
    # private_key = '8'
    
    # signature = get_signature(from_address, private_key)
    # amount, volume, rank = get_airdrop_info(from_address, signature)
    # print("Total Allocation:", amount)
    # print("Volume Traded:", volume)
    # print("Rank:", rank)

    with open('wallets1.txt', 'r') as file:
        lines = file.readlines()
    
    
    for line in lines:
        address, private_key = line.strip().split(',')
        signature = get_signature(address, private_key)
        amount, volume, rank = get_airdrop_info(address, signature)
        print("Wallet Address:", address)
        print("Total Allocation:", amount)
        print("Volume Traded:", volume)
        print("Rank:", rank)
        print("--------------------")