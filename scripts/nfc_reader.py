import nfc # For reading NFC tags

# Usage: This script is used to output the NFC tag code associated
#        with each tag
# Example run: "nfc_reader.py"

def nfc_reader_on_tag_connect(tag):
    print(tag.identifier.hex())
    return True

def nfc_reader_on_tag_release(tag):
    return False

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-release': nfc_reader_on_tag_release, 'on-connect': nfc_reader_on_tag_connect})