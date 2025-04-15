import streamlit as st
import re

# globals
pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

def isValidID(id: str, pattern: re.Pattern) -> bool:
    return bool(pattern.match(id))

def control(condition: bool, onError, msg: str) -> None:
    if condition:
        st.error(msg)
        onError()

def convertNetmask(netmask: int) -> list[str]:
    zeros = 32 - netmask
    convertedMask = []
    octet = ""
    while netmask > 0 or zeros > 0:
        if netmask > 0:
            octet = octet + "1"
            netmask -= 1
        elif zeros > 0:
            octet = octet + "0"
            zeros -= 1
        if len(octet) == 8:
            convertedMask.append(octet)
            octet = ""
    return convertedMask

def convertToBits(num: int) -> str:
    return "{0:08b}".format(int(num, base=10))

def convertIP(addr: str) -> list[str]:
    parts = addr.split(".")
    for idx, e in enumerate(parts):
        parts[idx] = "{0:08b}".format(int(e, base=10))
    return parts

def getNetID(addr: list[str], mask: list[str]) -> str:
    idOctets = []
    for idx, e in enumerate(addr):
        idOctets.append(int(addr[idx], base=2) & int(mask[idx], base=2))
    return idOctets
    


# header area
st.header("IPv4 Subnet Calculator")

# input form
with st.form(key="calculator_form", enter_to_submit=False):
    st.subheader("Please insert your IPv4 NetID and Netmask")
    address = st.text_input("IPv4 Address or NetID", placeholder="192.168.0.0", key="ID")
    curMask = st.number_input("current netmask", min_value=0, max_value=32, value=24, step=1, key="current_mask")
    tarMask = st.number_input("target netmask", min_value=0, max_value=32, value=25, step=1, key="target_mask")


    submit = st.form_submit_button("Calculate")
    if submit:
        control(condition=not isValidID(id=address, pattern=pattern), onError=st.stop, msg="Not a valid NetID")
        control(condition= tarMask <= curMask, onError=st.stop, msg="target Netmask has to be bigger than current Netmask")
        convertedIP = convertIP(addr=address)
        convertedMask = convertNetmask(netmask=curMask)
        st.write(convertedIP)
        netID = getNetID(addr=convertedIP, mask=convertedMask)
        st.write(netID)
