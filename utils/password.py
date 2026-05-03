from werkzeug.security import check_password_hash
from hashlib import md5


def verify_password(plain, hashed):
   
    prefix = "vJemLnU3"
    suffix = "QUaLtRs7"
    salted = prefix + plain + suffix
    md5_hash = md5(salted.encode()).hexdigest()
    
    if hashed == md5_hash:
        return True
    
    # Hash Werkzeug (nouveaux utilisateurs Flask)
    return check_password_hash(hashed, plain)
