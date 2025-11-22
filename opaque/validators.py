import re
from typing import Optional

class Validator:
    @staticmethod
    def validate(value: str) -> bool:
        raise NotImplementedError

# ==================== BRASIL ====================

class CPFValidator(Validator):
    @staticmethod
    def validate(cpf: str) -> bool:
        """Validates Brazilian CPF with or without formatting."""
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
        """Validates Brazilian CNPJ with or without formatting."""
        cnpj = re.sub(r'\D', '', str(cnpj))
        
        if len(cnpj) != 14 or len(set(cnpj)) == 1:
            return False
            
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (sum_val % 11)
        digit1 = 0 if digit1 > 9 else digit1
        
        if int(cnpj[12]) != digit1:
            return False
            
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (sum_val % 11)
        digit2 = 0 if digit2 > 9 else digit2
        
        return int(cnpj[13]) == digit2

class RGValidator(Validator):
    @staticmethod
    def validate(rg: str) -> bool:
        """Validates Brazilian RG (basic format check - varies by state)."""
        rg = re.sub(r'\D', '', str(rg))
        # RG can be 7-9 digits depending on state
        return 7 <= len(rg) <= 9

class CNHValidator(Validator):
    @staticmethod
    def validate(cnh: str) -> bool:
        """Validates Brazilian CNH (Driver's License) - Format check."""
        cnh = re.sub(r'\D', '', str(cnh))
        return len(cnh) == 11 and len(set(cnh)) > 1

class RenavamValidator(Validator):
    @staticmethod
    def validate(renavam: str) -> bool:
        """Validates Brazilian RENAVAM (Vehicle Registration) - Format check."""
        renavam = re.sub(r'\D', '', str(renavam))
        return len(renavam) == 11

class PlacaMercosulValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Mercosul license plate format (ABC1D23)."""
        placa = placa.upper().replace('-', '').replace(' ', '')
        return bool(re.match(r'^[A-Z]{3}\d[A-Z]\d{2}$', placa))

class PlacaBrasilAntigaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates old Brazilian license plate format (ABC-1234)."""
        placa = placa.upper().replace('-', '').replace(' ', '')
        return bool(re.match(r'^[A-Z]{3}\d{4}$', placa))

class PixValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        """Validates Brazilian Pix keys."""
        # UUID
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', key, re.IGNORECASE):
            return True
        # Email
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', key):
            return True
        # Phone (+55...)
        if re.match(r'^\+55\d{10,11}$', key):
            return True
        # CPF/CNPJ are validated separately
        return False

# ==================== ARGENTINA ====================

class CUILValidator(Validator):
    @staticmethod
    def validate(cuil: str) -> bool:
        """Validates Argentine CUIL/CUIT - Format check."""
        cuil = re.sub(r'\D', '', str(cuil))
        return len(cuil) == 11

class DNIArgentinaValidator(Validator):
    @staticmethod
    def validate(dni: str) -> bool:
        """Validates Argentine DNI."""
        dni = re.sub(r'\D', '', str(dni))
        return 7 <= len(dni) <= 8

# ==================== CHILE ====================

class RUTValidator(Validator):
    @staticmethod
    def validate(rut: str) -> bool:
        """Validates Chilean RUT."""
        rut = rut.replace('.', '').replace('-', '').upper()
        
        if len(rut) < 2:
            return False
            
        body = rut[:-1]
        dv = rut[-1]
        
        if not body.isdigit():
            return False
            
        sum_val = 0
        multiplier = 2
        
        for digit in reversed(body):
            sum_val += int(digit) * multiplier
            multiplier = multiplier + 1 if multiplier < 7 else 2
            
        expected_dv = 11 - (sum_val % 11)
        
        if expected_dv == 11:
            expected_dv = '0'
        elif expected_dv == 10:
            expected_dv = 'K'
        else:
            expected_dv = str(expected_dv)
            
        return dv == expected_dv

# ==================== COLOMBIA ====================

class CEDULAColombiaValidator(Validator):
    @staticmethod
    def validate(cedula: str) -> bool:
        """Validates Colombian Cédula."""
        cedula = re.sub(r'\D', '', str(cedula))
        return 6 <= len(cedula) <= 10

class NITColombiaValidator(Validator):
    @staticmethod
    def validate(nit: str) -> bool:
        """Validates Colombian NIT - Format check."""
        nit = re.sub(r'\D', '', str(nit))
        return len(nit) >= 9

# ==================== PERU ====================

class DNIPeruValidator(Validator):
    @staticmethod
    def validate(dni: str) -> bool:
        """Validates Peruvian DNI."""
        dni = re.sub(r'\D', '', str(dni))
        return len(dni) == 8

class RUCPeruValidator(Validator):
    @staticmethod
    def validate(ruc: str) -> bool:
        """Validates Peruvian RUC - Format check."""
        ruc = re.sub(r'\D', '', str(ruc))
        
        if len(ruc) != 11:
            return False
            
        # Type validation (first 2 digits)
        return ruc[:2] in ['10', '15', '17', '20']

# ==================== URUGUAY ====================

class CIUruguayValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        """Validates Uruguayan CI - Format check."""
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 8

class RUTUruguayValidator(Validator):
    @staticmethod
    def validate(rut: str) -> bool:
        """Validates Uruguayan RUT."""
        rut = re.sub(r'\D', '', str(rut))
        return len(rut) == 12

# ==================== VENEZUELA ====================

class CIVenezuelaValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        """Validates Venezuelan CI."""
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 9

class RIFValidator(Validator):
    @staticmethod
    def validate(rif: str) -> bool:
        """Validates Venezuelan RIF."""
        rif = rif.upper().replace('-', '').replace('.', '').replace(' ', '')
        
        if len(rif) < 9:
            return False
            
        # Must start with V, E, J, P, or G
        if rif[0] not in ['V', 'E', 'J', 'P', 'G']:
            return False
            
        numbers = rif[1:]
        if not numbers.isdigit():
            return False
            
        return len(numbers) >= 7

# ==================== ECUADOR ====================

class CEDULAEcuadorValidator(Validator):
    @staticmethod
    def validate(cedula: str) -> bool:
        """Validates Ecuadorian Cédula."""
        cedula = re.sub(r'\D', '', str(cedula))
        
        if len(cedula) != 10:
            return False
            
        # Province code (first 2 digits)
        province = int(cedula[:2])
        if province < 1 or province > 24:
            return False
            
        # Verification digit calculation
        coefficients = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        sum_val = 0
        
        for i in range(9):
            product = int(cedula[i]) * coefficients[i]
            sum_val += product if product < 10 else product - 9
            
        check_digit = (10 - (sum_val % 10)) % 10
        
        return int(cedula[9]) == check_digit

class RUCEcuadorValidator(Validator):
    @staticmethod
    def validate(ruc: str) -> bool:
        """Validates Ecuadorian RUC."""
        ruc = re.sub(r'\D', '', str(ruc))
        return len(ruc) == 13

# ==================== BOLIVIA ====================

class CIBoliviaValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        """Validates Bolivian CI."""
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 9

class NITBoliviaValidator(Validator):
    @staticmethod
    def validate(nit: str) -> bool:
        """Validates Bolivian NIT."""
        nit = re.sub(r'\D', '', str(nit))
        return len(nit) >= 7

# ==================== PARAGUAY ====================

class CIParaguayValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        """Validates Paraguayan CI."""
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 8

class RUCParaguayValidator(Validator):
    @staticmethod
    def validate(ruc: str) -> bool:
        """Validates Paraguayan RUC."""
        ruc = re.sub(r'\D', '', str(ruc))
        return len(ruc) >= 6

# ==================== INTERNATIONAL ====================

class CreditCardValidator(Validator):
    @staticmethod
    def validate(card_number: str) -> bool:
        """Validates credit card using Luhn algorithm."""
        card_number = re.sub(r'\D', '', str(card_number))
        if not card_number or len(card_number) < 13:
            return False
            
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

class IBANValidator(Validator):
    @staticmethod
    def validate(iban: str) -> bool:
        """Validates International Bank Account Number."""
        iban = iban.replace(' ', '').replace('-', '').upper()
        
        if len(iban) < 15 or len(iban) > 34:
            return False
            
        # Move first 4 chars to end
        rearranged = iban[4:] + iban[:4]
        
        # Replace letters with numbers (A=10, B=11, etc.)
        numeric = ''
        for char in rearranged:
            if char.isdigit():
                numeric += char
            else:
                numeric += str(ord(char) - ord('A') + 10)
                
        return int(numeric) % 97 == 1

class EmailValidator(Validator):
    @staticmethod
    def validate(email: str) -> bool:
        """Validates email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

class PhoneValidator(Validator):
    @staticmethod
    def validate(phone: str) -> bool:
        """Validates international phone format."""
        phone = re.sub(r'\D', '', phone)
        return 8 <= len(phone) <= 15

class PassportValidator(Validator):
    @staticmethod
    def validate(passport: str) -> bool:
        """Validates passport format (alphanumeric, 6-9 chars)."""
        passport = passport.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z0-9]{6,9}$', passport))

# ==================== VALIDATORS REGISTRY ====================

class Validators:
    class BR:
        """Brazilian validators"""
        CPF = CPFValidator
        CNPJ = CNPJValidator
        RG = RGValidator
        CNH = CNHValidator
        RENAVAM = RenavamValidator
        PIX = PixValidator
        PLACA_MERCOSUL = PlacaMercosulValidator
        PLACA_ANTIGA = PlacaBrasilAntigaValidator
    
    class AR:
        """Argentine validators"""
        CUIL = CUILValidator
        CUIT = CUILValidator  # Same as CUIL
        DNI = DNIArgentinaValidator
    
    class CL:
        """Chilean validators"""
        RUT = RUTValidator
    
    class CO:
        """Colombian validators"""
        CEDULA = CEDULAColombiaValidator
        NIT = NITColombiaValidator
    
    class PE:
        """Peruvian validators"""
        DNI = DNIPeruValidator
        RUC = RUCPeruValidator
    
    class UY:
        """Uruguayan validators"""
        CI = CIUruguayValidator
        RUT = RUTUruguayValidator
    
    class VE:
        """Venezuelan validators"""
        CI = CIVenezuelaValidator
        RIF = RIFValidator
    
    class EC:
        """Ecuadorian validators"""
        CEDULA = CEDULAEcuadorValidator
        RUC = RUCEcuadorValidator
    
    class BO:
        """Bolivian validators"""
        CI = CIBoliviaValidator
        NIT = NITBoliviaValidator
    
    class PY:
        """Paraguayan validators"""
        CI = CIParaguayValidator
        RUC = RUCParaguayValidator
    
    class FINANCE:
        """Financial validators"""
        CREDIT_CARD = CreditCardValidator
        IBAN = IBANValidator
    
    class INTERNATIONAL:
        """International validators"""
        EMAIL = EmailValidator
        PHONE = PhoneValidator
        PASSPORT = PassportValidator
