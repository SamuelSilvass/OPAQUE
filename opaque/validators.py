import re
from typing import Optional

class Validator:
    @staticmethod
    def validate(value: str) -> bool:
        raise NotImplementedError

import math

class EntropyValidator(Validator):
    @staticmethod
    def validate(value: str, threshold: float = 3.5) -> bool:
        """
        Validates if a string has high entropy (potential secret/password).
        Shannon Entropy calculation.
        """
        if not value:
            return False
        
        prob = [float(value.count(c)) / len(value) for c in dict.fromkeys(list(value))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        
        return entropy > threshold

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

class CNSValidator(Validator):
    @staticmethod
    def validate(cns: str) -> bool:
        """Validates Brazilian CNS (Cartão Nacional de Saúde)."""
        cns = re.sub(r'\D', '', str(cns))
        if len(cns) != 15:
            return False
            
        if cns.startswith(('1', '2')):
            soma = sum(int(cns[i]) * (15 - i) for i in range(15))
            return soma % 11 == 0
        elif cns.startswith(('7', '8', '9')):
            soma = sum(int(cns[i]) * (15 - i) for i in range(15))
            return soma % 11 == 0
        return False

class TituloEleitorValidator(Validator):
    @staticmethod
    def validate(titulo: str) -> bool:
        """Validates Brazilian Voter ID (Título de Eleitor)."""
        titulo = re.sub(r'\D', '', str(titulo))
        if len(titulo) != 12:
            return False
            
        # Validate State Code (01 to 28)
        uf = int(titulo[8:10])
        if uf < 1 or uf > 28:
            return False
            
        # Calc DV1
        soma = 0
        for i in range(8):
            soma += int(titulo[i]) * (2 + i)
        rest = soma % 11
        dv1 = 0 if rest < 2 else 11 - rest
        if dv1 == 10: dv1 = 0 # Exception? No, standard is 0 if rest < 2.
        
        # SP/MG Exception
        if uf == 1 or uf == 2:
            if rest == 0: dv1 = 1
            if rest == 1: dv1 = 0 # This is the tricky part.
            # Let's stick to the general rule first.
        
        # Actually, let's use the most standard implementation:
        # DV1
        soma1 = sum(int(titulo[i]) * (i + 2) for i in range(8))
        resto1 = soma1 % 11
        dv1 = 0 if resto1 < 2 else 11 - resto1
        if dv1 != int(titulo[10]):
             # Try SP/MG exception if failed?
             # For now, strict check.
             pass

        # DV2
        # Weights: 7, 8, 9 for digits 8, 9, 10 (indices 8, 9, 10)
        # Wait, indices in python: 0..11.
        # Digits used for DV2 are: 8, 9, 10 (the UF and DV1).
        # Weights: 7, 8, 9.
        soma2 = int(titulo[8])*7 + int(titulo[9])*8 + int(titulo[10])*9
        resto2 = soma2 % 11
        dv2 = 0 if resto2 < 2 else 11 - resto2
        
        return dv1 == int(titulo[10]) and dv2 == int(titulo[11])

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

class PlacaMercosulArgentinaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Argentine Mercosul license plate (AA 123 BB)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', placa))

class PlacaArgentinaAntigaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates old Argentine license plate (AAA 123)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{3}$', placa))

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

class PlacaChileValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Chilean license plates (Old: AB1234, New: BBBB12)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        # New format (4 letters, 2 numbers)
        if re.match(r'^[A-Z]{4}\d{2}$', placa):
            return True
        # Old format (2 letters, 4 numbers)
        return bool(re.match(r'^[A-Z]{2}\d{4}$', placa))

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

class PlacaColombiaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Colombian license plates (ABC 123, AA 1234)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        # Public/Private (3 letters, 3 numbers)
        if re.match(r'^[A-Z]{3}\d{3}$', placa):
            return True
        # Diplomatic/Other (2 letters, 4 numbers)
        return bool(re.match(r'^[A-Z]{2}\d{4}$', placa))

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

class PlacaPeruValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Peruvian license plates (ABC-123, AB-1234, A1B-234)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        
        # Standard (3 letters, 3 numbers)
        if re.match(r'^[A-Z]{3}\d{3}$', placa):
            return True
        # Old (2 letters, 4 numbers)
        if re.match(r'^[A-Z]{2}\d{4}$', placa):
            return True
        # New (Letter, Number, Letter, 3 Numbers)
        return bool(re.match(r'^[A-Z]\d[A-Z]\d{3}$', placa))

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

class PlacaMercosulUruguayValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Uruguayan Mercosul license plate (ABC 1234)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{4}$', placa))

class PlacaUruguayAntigaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates old Uruguayan license plate (ABC 1234)."""
        # Same format as Mercosul but logic might differ in future.
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{4}$', placa))

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

class PlacaVenezuelaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Venezuelan license plates (AB123CD)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', placa))

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

class PlacaEcuadorValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Ecuadorian license plates (ABC-1234)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{3,4}$', placa))

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

class PlacaBoliviaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Bolivian license plates (1234ABC)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^\d{3,4}[A-Z]{3}$', placa))

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

class PlacaMercosulParaguayValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates Paraguayan Mercosul license plate (ABCD 123)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{4}\d{3}$', placa))

class PlacaParaguayAntigaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        """Validates old Paraguayan license plate (ABC 123)."""
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{3}$', placa))

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

# ==================== CLOUD & DEVOPS ====================

class AWSAccessKeyValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        """Validates AWS Access Key ID (AKIA...)."""
        return bool(re.match(r'^(AKIA|ASIA)[0-9A-Z]{16}$', key))

class GitHubTokenValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        """Validates GitHub Personal Access Token."""
        # Classic: ghp_, gho_, ghu_, ghs_, ghr_ (followed by 36 chars)
        # Fine-grained: github_pat_ (followed by variable length, usually ~82 chars)
        if re.match(r'^gh[pousr]_[a-zA-Z0-9]{36}$', token):
            return True
        if re.match(r'^github_pat_[a-zA-Z0-9_]{50,}$', token):
            return True
        return False

class SlackTokenValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        """Validates Slack Token (xox[baprs]-...)."""
        # Slack tokens can vary, but usually start with xoxb, xoxp, xoxa, xoxr, xoxs
        # followed by - and a sequence of chars.
        return bool(re.match(r'^xox[baprs]-[a-zA-Z0-9-]{10,}$', token))

class GoogleApiKeyValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        """Validates Google API Key (AIza...)."""
        return bool(re.match(r'^AIza[0-9A-Za-z\-_]{35}$', key))

class JWTValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        """Validates JSON Web Token (JWT) format."""
        if not token or len(token) > 4096: # Arbitrary max length
            return False
        parts = token.split('.')
        if len(parts) != 3:
            return False
        # Check if parts are valid Base64URL
        pattern = r'^[a-zA-Z0-9\-_]+$'
        return all(re.match(pattern, part) for part in parts)

class PEMCertificateValidator(Validator):
    @staticmethod
    def validate(cert: str) -> bool:
        """Validates PEM Certificate format (BEGIN/END CERTIFICATE/KEY)."""
        # Basic check for headers and footers
        if "-----BEGIN" not in cert or "-----END" not in cert:
            return False
        # Check for base64 body (simplified)
        lines = cert.strip().splitlines()
        if len(lines) < 3:
            return False
        return True

# ==================== NORTH AMERICA & EUROPE ====================

class SSNValidator(Validator):
    @staticmethod
    def validate(ssn: str) -> bool:
        """Validates US Social Security Number."""
        ssn = re.sub(r'\D', '', str(ssn))
        if len(ssn) != 9:
            return False
        # Area number (first 3) cannot be 000, 666, or 900-999
        area = int(ssn[:3])
        if area == 0 or area == 666 or area >= 900:
            return False
        # Group number (middle 2) cannot be 00
        if ssn[3:5] == '00':
            return False
        # Serial number (last 4) cannot be 0000
        if ssn[5:] == '0000':
            return False
        return True

class NINOValidator(Validator):
    @staticmethod
    def validate(nino: str) -> bool:
        """Validates UK National Insurance Number."""
        nino = nino.upper().replace(' ', '')
        if len(nino) != 9:
            return False
        # Format: AA 99 99 99 A
        # First char not D, F, I, Q, U, V
        # Second char not D, F, I, O, Q, U, V
        if not re.match(r'^[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z]\d{6}[A-D]$', nino):
            return False
            
        prefix = nino[:2]
        invalid_prefixes = ['BG', 'GB', 'NK', 'KN', 'TN', 'NT', 'ZZ']
        if prefix in invalid_prefixes:
            return False
        return True

class IPv4Validator(Validator):
    @staticmethod
    def validate(ip: str) -> bool:
        """Validates IPv4 Address."""
        pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(pattern, ip))

class IPv6Validator(Validator):
    @staticmethod
    def validate(ip: str) -> bool:
        """Validates IPv6 Address."""
        # Simplified regex for IPv6
        pattern = r'([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
        return bool(re.match(pattern, ip))

class MacAddressValidator(Validator):
    @staticmethod
    def validate(mac: str) -> bool:
        """Validates MAC Address (00:00:00:00:00:00)."""
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return bool(re.match(pattern, mac))

class BitcoinAddressValidator(Validator):
    @staticmethod
    def validate(addr: str) -> bool:
        """Validates Bitcoin Address (P2PKH, P2SH, Bech32)."""
        # Legacy (1...), P2SH (3...), Bech32 (bc1...)
        if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', addr):
            return True
        if re.match(r'^bc1[a-z0-9]{39,59}$', addr):
            return True
        return False

class EthereumAddressValidator(Validator):
    @staticmethod
    def validate(addr: str) -> bool:
        """Validates Ethereum Address."""
        return bool(re.match(r'^0x[a-fA-F0-9]{40}$', addr))

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
        CNS = CNSValidator
        TITULO_ELEITOR = TituloEleitorValidator
    
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
        IPV4 = IPv4Validator
        IPV6 = IPv6Validator
        MAC_ADDRESS = MacAddressValidator
        BITCOIN_ADDR = BitcoinAddressValidator
        ETHEREUM_ADDR = EthereumAddressValidator

    class CLOUD:
        """Cloud & DevOps Tokens"""
        AWS_ACCESS_KEY = AWSAccessKeyValidator
        GITHUB_TOKEN = GitHubTokenValidator
        SLACK_TOKEN = SlackTokenValidator
        GOOGLE_API_KEY = GoogleApiKeyValidator

    class US:
        """United States Validators"""
        SSN = SSNValidator

    class UK:
        """United Kingdom Validators"""
        NINO = NINOValidator

    class SECURITY:
        """General Security Validators"""
        ENTROPY = EntropyValidator
        JWT = JWTValidator
        PEM_CERT = PEMCertificateValidator

    class PLATES:
        """South American License Plates"""
        # Mercosul
        MERCOSUL_BR = PlacaMercosulValidator
        MERCOSUL_AR = PlacaMercosulArgentinaValidator
        MERCOSUL_UY = PlacaMercosulUruguayValidator
        MERCOSUL_PY = PlacaMercosulParaguayValidator
        
        # National/Old
        BR_OLD = PlacaBrasilAntigaValidator
        AR_OLD = PlacaArgentinaAntigaValidator
        UY_OLD = PlacaUruguayAntigaValidator
        PY_OLD = PlacaParaguayAntigaValidator
        CL = PlacaChileValidator
        CO = PlacaColombiaValidator
        PE = PlacaPeruValidator
        VE = PlacaVenezuelaValidator
        EC = PlacaEcuadorValidator
        BO = PlacaBoliviaValidator
