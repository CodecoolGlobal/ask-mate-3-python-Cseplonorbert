import bcrypt


def allowed_image(filename, allowed_extensions):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_extensions:
        return True
    else:
        return False


def generate_hash_password(plain_text_password):
    hashed_password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    return hashed_password


def check_hash_password(hashed_password, plain_text_password):
    checked_password = bcrypt.check_password_hash(hashed_password, plain_text_password)
    return checked_password
