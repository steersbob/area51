from brewblox_codec_spark import codec

b = codec.encode(10, {
    'command': {},
    'address': ['AA', 'BB']
})

print(b)
