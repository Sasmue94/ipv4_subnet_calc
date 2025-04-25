import streamlit as st
from ipv4 import IPv4
from collections.abc import Callable
import re

if __name__ == "__main__":
    # globals
    __pattern: re.Pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

    # check if ip is valid
    def is_valid_id(id: str, pattern: re.Pattern) -> bool:
        return bool(pattern.match(id))

    # check if condition is met, show error message and call a function if not
    def control(condition: bool, onError: Callable, msg: str) -> None:
        if condition:
            st.error(msg)
            onError()

    # header areal
    st.header("IPv4 Subnet Calculator")

    # input form
    with st.form(key="calculator_form", enter_to_submit=False):
        st.subheader("Please insert your IPv4 Address of Net-Id and Prefix")
        address: str = st.text_input("IPv4 Address or NetID", placeholder="192.168.0.0", key="ID")
        current_prefix: int = st.number_input("current Prefix", min_value=0, max_value=32, value=24, step=1, key="current_prefix")
        target_prefix: int = st.number_input("target Prefix", min_value=0, max_value=32, value=25, step=1, key="target_prefix")


        submit = st.form_submit_button("Calculate")
        if submit:
            control(condition=not is_valid_id(id=address, pattern=__pattern), onError=st.stop, msg="Not a valid NetID")
            control(condition= target_prefix <= current_prefix, onError=st.stop, msg="target Netmask has to be bigger than current Netmask")
            ip: IPv4 = IPv4(ip=address, prefix=current_prefix)
            st.divider()
            st.write(f"current IPv4-Network: {ip.get_net_id()}/{ip.get_prefix()}")
            st.write(f"current Prefix evaluates to the following Subnetmask: {ip.get_dec_mask()}")
            st.write(f"current Number of hosts: {ip.get_current_net_size() - 2}")
            st.divider()
            st.subheader("After subnetting the following applies:")
            st.write(f"Number of hosts per network: {ip.get_target_net_size(target_prefix=target_prefix) - 2}")
            st.write(f"Number of networks: {ip.get_no_of_subnets(target_prefix=target_prefix)}")
            st.divider()
            st.subheader("List of Subnets:")
            subnets = ip.subnet(target_prefix=target_prefix)
            for subnet in subnets:
                st.write(subnet)
