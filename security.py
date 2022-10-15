from password_validator import PasswordValidator

password_validator = PasswordValidator()
password_validator.min(8)
password_validator.max(20)
password_validator.has().uppercase()
password_validator.has().lowercase()
password_validator.has().digits()
password_validator.has().symbols()
password_validator.has().no().spaces()
