import hashlib
import random
from time import time


def get_random_string(
    length=12,
    allowed_chars="abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    secret_key: str = None,
    using_sysrandom: bool = True,
):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        random.seed(
            hashlib.sha256(
                ("{}{}{}".format(random.getstate(), time.time(), secret_key)).encode("utf-8")
            ).digest()
        )
    return "".join(random.choice(allowed_chars) for i in range(length))
