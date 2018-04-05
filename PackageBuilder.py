from packageTypeEnums import PackageType

def build_package(package):
    pass
    return data
    
def create_request(address, recursive=True, req_type=PackageType.A,
                   req_class='IN'):
    dns = b''
    dns += b'\xAB\xCD'  # transaction id
    flag = 0
    flag |= int(recursive)
    flag *= 2 ** 8
    dns += flag.to_bytes(2, 'big')
    dns += (1).to_bytes(2, 'big')  # questions
    dns += (0).to_bytes(2, 'big')  # responses
    dns += (0).to_bytes(2, 'big')  # authority resource records
    dns += (0).to_bytes(2, 'big')  # additional resource records
    
    dns += encode_address_with_hex_prefixes(address)
    dns += req_type.value
    if req_class == 'IN':
        dns += ((1).to_bytes(2, 'big'))
    else:
        raise ValueError("Only IN class request are supported")
    return dns


def encode_address_with_hex_prefixes(address):
    ans = b''
    for word in address.split('.'):
        ans += bytes([len(word)]) + word.encode('ASCII')
    ans += b'\x00'
    return ans
