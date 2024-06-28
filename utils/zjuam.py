import requests
import re

class ZJUAM:
    """
    ZJUAM is a class that helps you login to ZJUAM.
    """

    def __init__(
        self,
        username: str,
        password: str
    ):
        self.username = username
        self.password = password
        self.session = requests.Session()
        
    def encode_password(self, modulus_str: str, exponent_str: str):
        """
        Encode the password with RSA encryption.
        
        - modulus_str: The modulus of the RSA public key in hexadecimal.
        - exponent_str: The exponent of the RSA public key in hexadecimal.
        
        Return the encoded password in hexadecimal.
        """
        # get the modulus and exponent in integer
        modulus = int(modulus_str, 16)
        exponent = int(exponent_str, 16)
        # encode the password
        password_hex = int(
            ''.join(
                format(ord(c), 'x') for c in self.password
            ),
            16
        )
        password_pow = pow(password_hex, exponent, modulus)
        password_enc = hex(password_pow)[2:].zfill(128)
        
        return password_enc
        
    def ipd_fetch(self):
        """
        Login to ZJUAM.
        
        Return the iPlanetDirectoryPro cookie.
        """
        # Access the login page first to get the cookies and execution
        try:
            login_page = self.session.get('https://zjuam.zju.edu.cn/cas/login')
            self.session.cookies.update(login_page.cookies)
            execution = re.search(r'name="execution" value="(.*?)"', login_page.text).group(1)
        except:
            raise Exception('zjuam: Failed to access the login page')
        
        # Get Public Key and encode the password
        try:
            public_key = self.session.get('https://zjuam.zju.edu.cn/cas/v2/getPubKey').json()
            modulus_str = public_key['modulus']
            exponent_str = public_key['exponent']
        except:
            raise Exception('zjuam: Failed to get the public key')
        password_enc = self.encode_password(modulus_str, exponent_str)
        
        # Login
        login_data = {
            'username': self.username,
            'password': password_enc,
            'execution': execution,
            '_eventId': 'submit'
        }
        login_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            login_response = self.session.post(
                'https://zjuam.zju.edu.cn/cas/login',
                allow_redirects=False,
                headers=login_headers,
                data=login_data
            )
        except:
            raise Exception('zjuam: Failed to access the login page')
        
        # try to get the iPlanetDirectoryPro cookie
        try:
            ipd = login_response.cookies['iPlanetDirectoryPro']
        except:
            raise Exception('zjuam: Login failed, check your username and password')
        
        return ipd
        