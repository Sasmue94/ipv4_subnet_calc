import re
class IPv4:
    def __init__(self, ip: str, prefix: int):
        self.ip = ip
        self.octet_list = ip.split(".")
        self.prefix = prefix
        self.__bitlength = 32
        self.__pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    
    def set_ip(self, ip: str):
        if bool(self.__pattern.match(ip)):
            self.ip = ip
            self.octet_list = ip.split(".")
        else:
            raise ValueError(f"{ip} is not a valid ip in range of 0.0.0.0 - 255.255.255.255")
    
    def get_ip(self) -> str:
        return self.ip
    
    def get_prefix(self) -> int:
        return self.prefix

    # returns a specified octet
    def get_bin_octet(self, idx: int) -> str:
        if idx >= 0 and idx < 4:
            return "{0:08b}".format(int(self.octet_list[idx], base=10))
        else:
            raise IndexError("Index out of range of ipv4: 0 - 3")
    
    # returns ip in binary
    def get_bin_ip(self):
        parts = []
        for e in self.octet_list:
            parts.append("{0:08b}".format(int(e)))
        return parts
    
    # return Net ID of current IP-Address
    def get_net_id(self) -> str:
        mask = self.get_bin_mask()
        idOctets = ""
        for idx, e in enumerate(self.octet_list):
            idOctets += str(int(self.octet_list[idx]) & int(mask[idx], base=2))
            if idx < 3:
                idOctets += "."
        return idOctets
    
    # return Net ID of current IP in binary
    def get_net_id_bin(self) -> list[str]:
        net_id = self.get_net_id().split(".")
        for idx, oct in enumerate(net_id):
            net_id[idx] = "{0:08b}".format(int(oct))
        return net_id
    
    # return subnetmask as binary
    def get_bin_mask(self) -> list[str]:
        zeros = self.__bitlength - self.prefix
        netmask = self.prefix
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
    
    # return subnet mask in decimal form
    def get_dec_mask(self) -> str:
        mask = self.get_bin_mask()
        mask_octets = ""
        for idx, e in enumerate(mask):
            mask_octets += str(int(e, base=2))
            if idx < 3:
                mask_octets += "."
        return mask_octets
    
    # return the number of ip addresses in the given Network
    # including NET-ID and Broadcast
    def get_current_net_size(self) -> int:
        return 2 ** (self.__bitlength - self.get_prefix())
    
    # return the number of ip addresses in the target Network
    # including NET-ID and Broadcast
    def get_target_net_size(self, target_prefix: int) -> int:
        return 2 ** (self.__bitlength - target_prefix)
    
    # retun number of subnets created when switching from current to target prefix
    def get_no_of_subnets(self, target_prefix: int) -> int:
        return int(self.get_current_net_size() / self.get_target_net_size(target_prefix=target_prefix))
    
    # return given prefix to binary subnet mask
    def convert_prefix_to_bin(self, mask: int) -> list[str]:
        zeros = self.__bitlength - mask
        convertedMask = []
        octet = ""
        while mask > 0 or zeros > 0:
            if mask > 0:
                octet = octet + "1"
                mask -= 1
            elif zeros > 0:
                octet = octet + "0"
                zeros -= 1
            if len(octet) == 8:
                convertedMask.append(octet)
                octet = ""
        return convertedMask

    # returns a list of subnets given a IP address, prefix and target prefix
    def subnet(self, target_prefix: int) -> list[int]:
        subnets = []
        no_of_nets = self.get_no_of_subnets(target_prefix=target_prefix)
        net_size = self.get_target_net_size(target_prefix=target_prefix)
        net_id_list = self.get_net_id_bin()
        net_id_bin = ""
        for oct in net_id_list:
            net_id_bin += oct
        i = 0
        net_id_bin = int(net_id_bin, 2)
        while i < no_of_nets:
            suffix = i * net_size
            subnet = "{0:032b}".format(int(net_id_bin | suffix))
            subnet = f"{int(subnet[0:8], 2)}.{int(subnet[8:16], 2)}.{int(subnet[16:24], 2)}.{int(subnet[24:32], 2)} /{target_prefix}"
            subnets.append(subnet)
            i += 1   

        return subnets 
        
        


