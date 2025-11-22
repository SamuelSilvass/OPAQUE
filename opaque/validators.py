import re

class Validator:
    @staticmethod
    def validate(value: str) -> bool:
        raise NotImplementedError

class CPFValidator(Validator):
    @staticmethod
    def validate(cpf: str) -> bool:
        # Remove non-digits
        cpf = re.sub(r'\D', '', str(cpf))
        
        if len(cpf) != 11 or len(set(cpf)) == 1:
            return False
            
        # First Digit
        sum_val = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum_val % 11)
        digit1 = 0 if digit1 > 9 else digit1
        
        if int(cpf[9]) != digit1:
            return False
            
        # Second Digit
        sum_val = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum_val % 11)
        digit2 = 0 if digit2 > 9 else digit2
        
        return int(cpf[10]) == digit2

class CNPJValidator(Validator):
    @staticmethod
    def validate(cnpj: str) -> bool:
        cnpj = re.sub(r'\D', '', str(cnpj))
        
        if len(cnpj) != 14 or len(set(cnpj)) == 1:
            return False
            
        # First Digit
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (sum_val % 11)
        digit1 = 0 if digit1 > 9 else digit1
        
        if int(cnpj[12]) != digit1:
            return False
            
        # Second Digit
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (sum_val % 11)
        digit2 = 0 if digit2 > 9 else digit2
        
        return int(cnpj[13]) == digit2

class CreditCardValidator(Validator):
    @staticmethod
    def validate(card_number: str) -> bool:
        card_number = re.sub(r'\D', '', str(card_number))
        if not card_number:
            return False
            
        # Luhn Algorithm
        digits = [int(d) for d in card_number]
        checksum = 0
        reverse_digits = digits[::-1]
        
        for i, d in enumerate(reverse_digits):
            if i % 2 == 1:
                doubled = d * 2
                checksum += doubled if doubled < 10 else doubled - 9
            else:
                checksum += d
                
        return checksum % 10 == 0

class PixValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        # Pix keys can be: CPF/CNPJ (already handled), Email, Phone, or Random (UUID)
        # This validator checks for the specific formats of Email, Phone (+55...), and UUID.
        
        # 1. Random Key (UUID)
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', key, re.IGNORECASE):
            return True
            
        # 2. Email
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', key):
            return True
            
        # 3. Phone (+55...)
        if re.match(r'^\+55\d{10,11}$', key):
            return True
            
        return False

class Validators:
    class BR:
        CPF = CPFValidator
        CNPJ = CNPJValidator
        PIX = PixValidator
    
    class FINANCE:
        CREDIT_CARD = CreditCardValidator
