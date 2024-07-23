"""nfc_reader.py prints out NFC tag code associated with NFC tag. """

# This script outputs the NFC tag code associated with each NFC tag scanned by the NFC reader.
#
# Example: [python nfc_reader.py]

import nfc  # For reading NFC tags.


def nfc_reader_on_tag_connect(tag):
    """Prints NFC tag code."""
    print(tag.identifier.hex())
    return True


def nfc_reader_on_tag_release(tag):  # pylint: disable=W0613
    """Ends NFC Connection."""
    return False


clf = nfc.ContactlessFrontend("usb")
clf.connect(rdwr={"on-release": nfc_reader_on_tag_release, "on-connect": nfc_reader_on_tag_connect})
