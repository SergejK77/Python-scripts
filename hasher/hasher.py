import hashlib


def do_hashes(hashValue):
    hashmd5 = hashlib.md5()
    hashmd5.update(hashValue.encode())
    print('MD5 Hash: ' + hashmd5.hexdigest())

    hashsha1 = hashlib.sha1();
    hashsha1.update(hashValue.encode())
    print('SHA1 Hash: ' + hashsha1.hexdigest())

    hashsha224 = hashlib.sha224()
    hashsha224.update(hashValue.encode())
    print('SHA224 Hash: ' + hashsha224.hexdigest())

    hashsha256 = hashlib.sha256()
    hashsha256.update(hashValue.encode())
    print('SHA256 Hash: ' + hashsha256.hexdigest())

    hashsha512 = hashlib.sha512()
    hashsha512.update(hashValue.encode())
    print('SHA512 Hash: ' + hashsha512.hexdigest())

    hashsha384 = hashlib.sha384()
    hashsha384.update(hashValue.encode())
    print('SHA384 Hash: ' + hashsha384.hexdigest())

if __name__ == "__main__":
    hash_val = input("Enter String to Hash: ")
    do_hashes(hash_val)
