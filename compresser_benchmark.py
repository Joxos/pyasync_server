import zlib, gzip, bz2, lzma
import time
from random import randint

if __name__ == '__main__':
    bytes_origin = b'''Life is too short to spend time with people who suck the happiness out of you. If someone wants you in their life, they'll make room for you. You shouldn't have to fight for a spot. Never, ever insist yourself to someone who continuously overlooks your worth. And remember, it's not the people that stand by your side when you're at your best, but the ones who stand beside you when you're at your worst that are your true friends.''' * 10000
    length = len(bytes_origin)
    print(f'Compress benchmark with {length} bytes data.')

    start = time.time()
    compressed_data = zlib.compress(bytes_origin)
    # print(compressed_data)
    end = time.time()
    print(f'Zlib: {end-start} seconds, {len(compressed_data)/length*100}%')

    start = time.time()
    compressed_data = gzip.compress(bytes_origin)
    # print(compressed_data)
    end = time.time()
    print(f'Gzip: {end-start} seconds, {len(compressed_data)/length*100}%')

    start = time.time()
    compressed_data = bz2.compress(bytes_origin)
    # print(compressed_data)
    end = time.time()
    print(f'Bz2: {end-start} seconds, {len(compressed_data)/length*100}%')

    start = time.time()
    compressed_data = lzma.compress(bytes_origin)
    # print(compressed_data)
    end = time.time()
    print(f'LZMA: {end-start} seconds, {len(compressed_data)/length*100}%')
