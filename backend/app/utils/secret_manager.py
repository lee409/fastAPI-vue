import secrets
import string


class SecretsManager:
    @staticmethod
    def generate_random_key(length):
        """生成指定长度的随机密钥"""
        return secrets.token_hex(length // 2)  # 每个十六进制字符对应4位，因此除以2

    @staticmethod
    def generate_random_string(length):
        """生成指定长度的随机字符串（包含大小写字母和数字）"""
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def generate_random_bytes(length):
        """生成指定长度的随机字节串"""
        return secrets.token_bytes(length)

# 示例密钥长度
key_length = 32

# 生成随机密钥
# random_key = SecretsManager.generate_random_key(key_length)
# print("生成的随机密钥:", random_key)
#
# # 示例随机字符串长度
# string_length = 20
#
# # 生成随机字符串
# random_string = SecretsManager.generate_random_string(string_length)
# print("生成的随机字符串:", random_string)
#
# # 示例随机字节串长度
# bytes_length = 16
#
# # 生成随机字节串
# random_bytes = SecretsManager.generate_random_bytes(bytes_length)
# print("生成的随机字节串:", random_bytes)
