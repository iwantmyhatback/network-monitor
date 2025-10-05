import os
from routeros_api import RouterOsApiPool
import json
import logging as log
from mikrotik.exceptions import *
import ssl

class RouterLogin:
    def __init__(self):
        log.debug(f"RouterLogin.__init__({self})")
        config = json.load(open('configuration/info.json'))
        log.debug(f"Loaded configuration/info.json -- Empty Check: {not bool(config)}")
        self.host = config.get('MIKROTIK_HOST')
        self.username = config.get('MIKROTIK_USER')
        self.password = config.get('MIKROTIK_PASS')
        self.api = None
        self.connection = None

    def connect(self):
        log.debug(f"RouterLogin.connect({self})")
        try:
            if not self.host or not self.username or not self.password:
                raise RouterConfigurationError("Router configuration is incomplete. Please check configuration/info.json.")

            # Create a custom SSL context to handle Anonymous TLS cipher
            # > API-SSL service is capable of working in two modes - with and without a certificate. 
            # > In the case no certificate is used in /ip service settings then an anonymous Diffie-Hellman cipher has to be used to establish a connection. 
            # > If a certificate is in use, a TLS session can be established.
            # Source: https://help.mikrotik.com/docs/spaces/ROS/pages/47579160/API#API-Initiallogin
            ssl_context = ssl.create_default_context()
            # Note that "SECLEVEL=0" is required for anonymous Diffie-Hellman cipher suites by OpenSSL 1.1.0 and later
            ssl_context.set_ciphers("ADH-AES256-SHA256:AECDH-AES128-SHA:ADH-AES256-SHA:!CAMELLIA:!NULL:@SECLEVEL=0")
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            # For RouterOS 7.19.6 it appears that TLS 1.2 is the highest supported version
            ssl_context.tls_version = ssl.PROTOCOL_TLSv1_2

            log.debug(f"Attempting connection to router at {self.host} with user {self.username}")
            self.api = RouterOsApiPool(
                host=self.host,
                username=self.username,
                password=self.password,
                plaintext_login=True,
                ssl_context=ssl_context
            )

            log.debug("Connection to router established successfully")
            self.connection = self.api.get_api()

            log.debug("Router API instance obtained successfully")
            return self.connection
        except Exception as e:
            log.error(f"Failed to connect to router: {str(e)}")
            return None

    def disconnect(self):
        log.debug(f"RouterLogin.disconnect({self})")
        if self.api:
            log.debug("Disconnecting from router")
            try:
                self.api.disconnect()
                log.debug("Successfully disconnected from router")
            except Exception as e:
                log.error(f"Error during disconnection: {str(e)}")

    def is_connected(self):
        log.debug(f"RouterLogin.is_connected({self})")
        return self.connection is not None