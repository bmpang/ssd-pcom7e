from password_validator import PasswordValidator

def validatePassword(password):
    meets_criteria = bool
    pw = PasswordValidator()
    pw.min(8).max(15).has().uppercase().has().lowercase().has().digits().has().symbols()
    meets_criteria = pw.validate(password)
    return meets_criteria