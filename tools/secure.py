from rest_framework import status

from tools.affine import affine_encrypt
from rest_framework.response import Response


def checkAPI(data):
    # lang = data['X-Language']
    # device_id = data['X-Device-Id']
    # device_os = data['X-Device-Os']
    # app_version = data['X-App-Version']
    # secure_code = data['X-App-Secure']
    # try:
    #     sec1 = affine_encrypt(str(device_os), (15, 8))
    #     sec2 = affine_encrypt(str(device_id), (13, 4))
    #     sec3 = affine_encrypt(str(app_version), (13, 5))
    #     secure_try = affine_encrypt(f"{sec1}{sec2}{sec3}.a7az1n", (13, 5))
    #     if secure_code != secure_try:
    #         return True
    #     return False
    # except:
        return False
