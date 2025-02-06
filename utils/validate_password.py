import re
from django.core.exceptions import ValidationError


def validate_password_strength(password):
    # تحقق من الحد الأدنى للطول (6 حروف على سبيل المثال)
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters long.")
    
    # تحقق من وجود حرف صغير
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    
    # تحقق من وجود حرف كبير
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    
    # تحقق من وجود رقم
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one number.")
    
    # تحقق من وجود رمز خاص
    if not re.search(r'[@#$%^&+=]', password):
        raise ValidationError("Password must contain at least one special character (@, #, $, %, ^, &, +, =).")
    
    # إذا لم تنطبق أي من الشروط السابقة، كلمة المرور قوية
    return password