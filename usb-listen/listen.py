import usb.core

dev = usb.core.find(idVendor=0x2b04)

# was it found?
if dev is None:
    raise ValueError('Device not found')

dev.reset()

# bmRequestType: host to device
# bmRequest: init
# wValue: not used
# wIndex: 70 (magic number)
# 64 buffer for response
dev.ctrl_transfer(0x40, 1, 0, 70, 64)

# bmRequestType: host to device
# bmRequest: send
# wValue: not used
# wIndex: 70 (magic number)
# 64 buffer for response
dev.ctrl_transfer(0x40, 3, 0, 70, 64)
