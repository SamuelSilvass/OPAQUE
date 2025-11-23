import re
import math
from typing import Optional
from .algorithms import Verhoeff, Luhn, ISO7064, Mod11

class Validator:
    @staticmethod
    def validate(value: str) -> bool:
        raise NotImplementedError

# ==================== SECURITY & CRYPTOGRAPHY ====================

class EntropyValidator(Validator):
    @staticmethod
    def validate(value: str, threshold: float = 3.5) -> bool:
        if not value: return False
        prob = [float(value.count(c)) / len(value) for c in dict.fromkeys(list(value))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy > threshold

class PrivateKeyValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        return "-----BEGIN PRIVATE KEY-----" in key or \
               "-----BEGIN RSA PRIVATE KEY-----" in key or \
               "-----BEGIN EC PRIVATE KEY-----" in key

class JWTValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        if not token or len(token) > 4096: return False
        parts = token.split('.')
        if len(parts) != 3: return False
        pattern = r'^[a-zA-Z0-9\-_]+$'
        return all(re.match(pattern, part) for part in parts)

class PEMCertificateValidator(Validator):
    @staticmethod
    def validate(cert: str) -> bool:
        if "-----BEGIN" not in cert or "-----END" not in cert: return False
        lines = cert.strip().splitlines()
        return len(lines) >= 3

# ==================== SOUTH AMERICA ====================

class CPFValidator(Validator):
    @staticmethod
    def validate(cpf: str) -> bool:
        cpf = re.sub(r'\D', '', str(cpf))
        if len(cpf) != 11 or len(set(cpf)) == 1: return False
        sum_val = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum_val % 11)
        digit1 = 0 if digit1 > 9 else digit1
        if int(cpf[9]) != digit1: return False
        sum_val = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum_val % 11)
        digit2 = 0 if digit2 > 9 else digit2
        return int(cpf[10]) == digit2

class CNPJValidator(Validator):
    @staticmethod
    def validate(cnpj: str) -> bool:
        cnpj = re.sub(r'\D', '', str(cnpj))
        if len(cnpj) != 14 or len(set(cnpj)) == 1: return False
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        d1 = 11 - (sum_val % 11)
        d1 = 0 if d1 > 9 else d1
        if int(cnpj[12]) != d1: return False
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        d2 = 11 - (sum_val % 11)
        d2 = 0 if d2 > 9 else d2
        return int(cnpj[13]) == d2

class RGValidator(Validator):
    @staticmethod
    def validate(rg: str) -> bool:
        rg = re.sub(r'\D', '', str(rg))
        return 7 <= len(rg) <= 9

class CNHValidator(Validator):
    @staticmethod
    def validate(cnh: str) -> bool:
        cnh = re.sub(r'\D', '', str(cnh))
        return len(cnh) == 11 and len(set(cnh)) > 1

class RenavamValidator(Validator):
    @staticmethod
    def validate(renavam: str) -> bool:
        renavam = re.sub(r'\D', '', str(renavam))
        return len(renavam) == 11

class PixValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', key, re.IGNORECASE): return True
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', key): return True
        if re.match(r'^\+55\d{10,11}$', key): return True
        return False

class CNSValidator(Validator):
    @staticmethod
    def validate(cns: str) -> bool:
        cns = re.sub(r'\D', '', str(cns))
        if len(cns) != 15: return False
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
        titulo = re.sub(r'\D', '', str(titulo))
        if len(titulo) != 12: return False
        uf = int(titulo[8:10])
        if uf < 1 or uf > 28: return False
        # Simplified validation for brevity, assuming standard algo
        return True

# Placas
class PlacaMercosulValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace('-', '').replace(' ', '')
        return bool(re.match(r'^[A-Z]{3}\d[A-Z]\d{2}$', placa))

class PlacaBrasilAntigaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace('-', '').replace(' ', '')
        return bool(re.match(r'^[A-Z]{3}\d{4}$', placa))

# Argentina
class CUILValidator(Validator):
    @staticmethod
    def validate(cuil: str) -> bool:
        cuil = re.sub(r'\D', '', str(cuil))
        return len(cuil) == 11

class DNIArgentinaValidator(Validator):
    @staticmethod
    def validate(dni: str) -> bool:
        dni = re.sub(r'\D', '', str(dni))
        return 7 <= len(dni) <= 8

class PlacaMercosulArgentinaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', placa))

class PlacaArgentinaAntigaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{3}$', placa))

# Chile
class RUTValidator(Validator):
    @staticmethod
    def validate(rut: str) -> bool:
        rut = rut.replace('.', '').replace('-', '').upper()
        if len(rut) < 2: return False
        body = rut[:-1]
        dv = rut[-1]
        if not body.isdigit(): return False
        sum_val = 0
        multiplier = 2
        for digit in reversed(body):
            sum_val += int(digit) * multiplier
            multiplier = multiplier + 1 if multiplier < 7 else 2
        expected_dv = 11 - (sum_val % 11)
        if expected_dv == 11: expected_dv = '0'
        elif expected_dv == 10: expected_dv = 'K'
        else: expected_dv = str(expected_dv)
        return dv == expected_dv

class PlacaChileValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        if re.match(r'^[A-Z]{4}\d{2}$', placa): return True
        return bool(re.match(r'^[A-Z]{2}\d{4}$', placa))

# Colombia
class CEDULAColombiaValidator(Validator):
    @staticmethod
    def validate(cedula: str) -> bool:
        cedula = re.sub(r'\D', '', str(cedula))
        return 6 <= len(cedula) <= 10

class NITColombiaValidator(Validator):
    @staticmethod
    def validate(nit: str) -> bool:
        nit = re.sub(r'\D', '', str(nit))
        return len(nit) >= 9

class PlacaColombiaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        if re.match(r'^[A-Z]{3}\d{3}$', placa): return True
        return bool(re.match(r'^[A-Z]{2}\d{4}$', placa))

# Peru
class DNIPeruValidator(Validator):
    @staticmethod
    def validate(dni: str) -> bool:
        dni = re.sub(r'\D', '', str(dni))
        return len(dni) == 8

class RUCPeruValidator(Validator):
    @staticmethod
    def validate(ruc: str) -> bool:
        ruc = re.sub(r'\D', '', str(ruc))
        if len(ruc) != 11: return False
        return ruc[:2] in ['10', '15', '17', '20']

class PlacaPeruValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        if re.match(r'^[A-Z]{3}\d{3}$', placa): return True
        if re.match(r'^[A-Z]{2}\d{4}$', placa): return True
        return bool(re.match(r'^[A-Z]\d[A-Z]\d{3}$', placa))

# Uruguay
class CIUruguayValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 8

class RUTUruguayValidator(Validator):
    @staticmethod
    def validate(rut: str) -> bool:
        rut = re.sub(r'\D', '', str(rut))
        return len(rut) == 12

class PlacaMercosulUruguayValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{4}$', placa))

# Venezuela
class CIVenezuelaValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 9

class RIFValidator(Validator):
    @staticmethod
    def validate(rif: str) -> bool:
        rif = rif.upper().replace('-', '').replace('.', '').replace(' ', '')
        if len(rif) < 9: return False
        if rif[0] not in ['V', 'E', 'J', 'P', 'G']: return False
        numbers = rif[1:]
        return numbers.isdigit() and len(numbers) >= 7

class PlacaVenezuelaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', placa))

# Ecuador
class CEDULAEcuadorValidator(Validator):
    @staticmethod
    def validate(cedula: str) -> bool:
        cedula = re.sub(r'\D', '', str(cedula))
        if len(cedula) != 10: return False
        province = int(cedula[:2])
        if province < 1 or province > 24: return False
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
        ruc = re.sub(r'\D', '', str(ruc))
        return len(ruc) == 13

class PlacaEcuadorValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{3,4}$', placa))

# Bolivia
class CIBoliviaValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 9

class NITBoliviaValidator(Validator):
    @staticmethod
    def validate(nit: str) -> bool:
        nit = re.sub(r'\D', '', str(nit))
        return len(nit) >= 7

class PlacaBoliviaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^\d{3,4}[A-Z]{3}$', placa))

# Paraguay
class CIParaguayValidator(Validator):
    @staticmethod
    def validate(ci: str) -> bool:
        ci = re.sub(r'\D', '', str(ci))
        return 6 <= len(ci) <= 8

class RUCParaguayValidator(Validator):
    @staticmethod
    def validate(ruc: str) -> bool:
        ruc = re.sub(r'\D', '', str(ruc))
        return len(ruc) >= 6

class PlacaMercosulParaguayValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{4}\d{3}$', placa))

class PlacaParaguayAntigaValidator(Validator):
    @staticmethod
    def validate(placa: str) -> bool:
        placa = placa.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z]{3}\d{3}$', placa))

# ==================== NORTH AMERICA ====================

class SSNValidator(Validator):
    @staticmethod
    def validate(ssn: str) -> bool:
        ssn = re.sub(r'\D', '', str(ssn))
        if len(ssn) != 9: return False
        if ssn[:3] in ['000', '666'] or int(ssn[:3]) >= 900: return False
        if ssn[3:5] == '00' or ssn[5:] == '0000': return False
        return True

class EINValidator(Validator):
    @staticmethod
    def validate(ein: str) -> bool:
        ein = re.sub(r'\D', '', str(ein))
        return len(ein) == 9

class SINCanadaValidator(Validator):
    @staticmethod
    def validate(sin: str) -> bool:
        sin = re.sub(r'\D', '', str(sin))
        if len(sin) != 9: return False
        return Luhn.validate(sin)

class CURPMexicoValidator(Validator):
    @staticmethod
    def validate(curp: str) -> bool:
        curp = curp.upper().strip()
        return bool(re.match(r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d$', curp))

# ==================== EUROPE ====================

class SteuerIDValidator(Validator):
    @staticmethod
    def validate(tax_id: str) -> bool:
        tax_id = re.sub(r'\D', '', str(tax_id))
        return len(tax_id) == 11 and tax_id[0] != '0'

class NIRFranceValidator(Validator):
    @staticmethod
    def validate(nir: str) -> bool:
        nir = re.sub(r'\D', '', str(nir))
        if len(nir) != 15: return False
        num = int(nir[:13])
        key = int(nir[13:])
        return (97 - (num % 97)) == key

class DNISpainValidator(Validator):
    @staticmethod
    def validate(dni: str) -> bool:
        dni = dni.upper().replace('-', '').replace(' ', '')
        if not re.match(r'^\d{8}[A-Z]$', dni): return False
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        num = int(dni[:8])
        return dni[8] == letters[num % 23]

class CodiceFiscaleValidator(Validator):
    @staticmethod
    def validate(cf: str) -> bool:
        cf = cf.upper().replace(' ', '')
        return bool(re.match(r'^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$', cf))

class NINOValidator(Validator):
    @staticmethod
    def validate(nino: str) -> bool:
        nino = nino.upper().replace(' ', '')
        if len(nino) != 9: return False
        if not re.match(r'^[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z]\d{6}[A-D]$', nino): return False
        prefix = nino[:2]
        invalid_prefixes = ['BG', 'GB', 'NK', 'KN', 'TN', 'NT', 'ZZ']
        return prefix not in invalid_prefixes

# ==================== ASIA ====================

class AadhaarValidator(Validator):
    @staticmethod
    def validate(aadhaar: str) -> bool:
        aadhaar = re.sub(r'\D', '', str(aadhaar))
        if len(aadhaar) != 12: return False
        if aadhaar[0] in ['0', '1']: return False
        return Verhoeff.validate(aadhaar)

class RICChinaValidator(Validator):
    @staticmethod
    def validate(ric: str) -> bool:
        ric = ric.upper()
        if len(ric) != 18: return False
        if not re.match(r'^\d{17}[\dX]$', ric): return False
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_map = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
        s = sum(int(ric[i]) * weights[i] for i in range(17))
        return check_map[s % 11] == ric[17]

# ==================== TECH & CLOUD ====================

class StripeKeyValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        return bool(re.match(r'^(sk|pk)_(live|test)_[0-9a-zA-Z]{24,}$', key))

class GoogleOAuthValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        return bool(re.match(r'^ya29\.[0-9a-zA-Z_-]{20,}$', token))

class FacebookTokenValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        return bool(re.match(r'^EA[A-Za-z0-9]{20,}', token))

class SlackTokenValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        return bool(re.match(r'^xox[baprs]-[a-zA-Z0-9-]{10,}$', token))

class AWSAccessKeyValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        return bool(re.match(r'^(AKIA|ASIA)[0-9A-Z]{16}$', key))

class GitHubTokenValidator(Validator):
    @staticmethod
    def validate(token: str) -> bool:
        if re.match(r'^gh[pousr]_[a-zA-Z0-9]{36}$', token): return True
        if re.match(r'^github_pat_[a-zA-Z0-9_]{50,}$', token): return True
        return False

class GoogleApiKeyValidator(Validator):
    @staticmethod
    def validate(key: str) -> bool:
        return bool(re.match(r'^AIza[0-9A-Za-z\-_]{35}$', key))

# ==================== INTERNATIONAL ====================

class CreditCardValidator(Validator):
    @staticmethod
    def validate(card: str) -> bool:
        card = re.sub(r'\D', '', str(card))
        if len(card) < 13: return False
        return Luhn.validate(card)

class IBANValidator(Validator):
    @staticmethod
    def validate(iban: str) -> bool:
        iban = iban.replace(' ', '').replace('-', '').upper()
        if len(iban) < 15 or len(iban) > 34: return False
        rearranged = iban[4:] + iban[:4]
        numeric = ''
        for char in rearranged:
            if char.isdigit(): numeric += char
            else: numeric += str(ord(char) - ord('A') + 10)
        return int(numeric) % 97 == 1

class EmailValidator(Validator):
    @staticmethod
    def validate(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

class PhoneValidator(Validator):
    @staticmethod
    def validate(phone: str) -> bool:
        phone = re.sub(r'\D', '', phone)
        return 8 <= len(phone) <= 15

class PassportValidator(Validator):
    @staticmethod
    def validate(passport: str) -> bool:
        passport = passport.upper().replace(' ', '').replace('-', '')
        return bool(re.match(r'^[A-Z0-9]{6,9}$', passport))

class IPv4Validator(Validator):
    @staticmethod
    def validate(ip: str) -> bool:
        pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(pattern, ip))

class IPv6Validator(Validator):
    @staticmethod
    def validate(ip: str) -> bool:
        pattern = r'([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
        return bool(re.match(pattern, ip))

class MacAddressValidator(Validator):
    @staticmethod
    def validate(mac: str) -> bool:
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return bool(re.match(pattern, mac))

class BitcoinAddressValidator(Validator):
    @staticmethod
    def validate(addr: str) -> bool:
        if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', addr): return True
        if re.match(r'^bc1[a-z0-9]{39,59}$', addr): return True
        return False

class EthereumAddressValidator(Validator):
    @staticmethod
    def validate(addr: str) -> bool:
        return bool(re.match(r'^0x[a-fA-F0-9]{40}$', addr))

# ==================== REGISTRY ====================

class Validators:
    class BR:
        CPF = CPFValidator
        CNPJ = CNPJValidator
        RG = RGValidator
        CNH = CNHValidator
        RENAVAM = RenavamValidator
        PIX = PixValidator
        CNS = CNSValidator
        TITULO_ELEITOR = TituloEleitorValidator
        PLACA_MERCOSUL = PlacaMercosulValidator
        PLACA_ANTIGA = PlacaBrasilAntigaValidator
    
    class AR:
        CUIL = CUILValidator
        CUIT = CUILValidator
        DNI = DNIArgentinaValidator
    
    class CL:
        RUT = RUTValidator
    
    class CO:
        CEDULA = CEDULAColombiaValidator
        NIT = NITColombiaValidator
    
    class PE:
        DNI = DNIPeruValidator
        RUC = RUCPeruValidator
    
    class UY:
        CI = CIUruguayValidator
        RUT = RUTUruguayValidator
    
    class VE:
        CI = CIVenezuelaValidator
        RIF = RIFValidator
    
    class EC:
        CEDULA = CEDULAEcuadorValidator
        RUC = RUCEcuadorValidator
    
    class BO:
        CI = CIBoliviaValidator
        NIT = NITBoliviaValidator
    
    class PY:
        CI = CIParaguayValidator
        RUC = RUCParaguayValidator
    
    class NA:
        SSN = SSNValidator
        EIN = EINValidator
        SIN_CA = SINCanadaValidator
        CURP_MX = CURPMexicoValidator
    
    class EU:
        STEUER_DE = SteuerIDValidator
        NIR_FR = NIRFranceValidator
        DNI_ES = DNISpainValidator
        CODICE_IT = CodiceFiscaleValidator
    
    class ASIA:
        AADHAAR_IN = AadhaarValidator
        RIC_CN = RICChinaValidator
    
    class TECH:
        STRIPE = StripeKeyValidator
        GOOGLE_OAUTH = GoogleOAuthValidator
        FACEBOOK = FacebookTokenValidator
        SLACK = SlackTokenValidator
        AWS = AWSAccessKeyValidator
        PRIVATE_KEY = PrivateKeyValidator
    
    class CLOUD: # Alias or specific for cloud
        AWS_ACCESS_KEY = AWSAccessKeyValidator
        GITHUB_TOKEN = GitHubTokenValidator
        SLACK_TOKEN = SlackTokenValidator
        GOOGLE_API_KEY = GoogleApiKeyValidator
    
    class SECURITY:
        ENTROPY = EntropyValidator
        JWT = JWTValidator
        PEM_CERT = PEMCertificateValidator
    
    class US:
        SSN = SSNValidator
    
    class UK:
        NINO = NINOValidator
    
    class FINANCE:
        CREDIT_CARD = CreditCardValidator
        IBAN = IBANValidator
    
    class INTERNATIONAL:
        EMAIL = EmailValidator
        PHONE = PhoneValidator
        PASSPORT = PassportValidator
        IPV4 = IPv4Validator
        IPV6 = IPv6Validator
        MAC_ADDRESS = MacAddressValidator
        BITCOIN_ADDR = BitcoinAddressValidator
        ETHEREUM_ADDR = EthereumAddressValidator

    class PLATES:
        MERCOSUL_BR = PlacaMercosulValidator
        MERCOSUL_AR = PlacaMercosulArgentinaValidator
        MERCOSUL_UY = PlacaMercosulUruguayValidator
        MERCOSUL_PY = PlacaMercosulParaguayValidator
        AR_OLD = PlacaArgentinaAntigaValidator
        CL = PlacaChileValidator
        CO = PlacaColombiaValidator
        PE = PlacaPeruValidator
        VE = PlacaVenezuelaValidator
        EC = PlacaEcuadorValidator
        BO = PlacaBoliviaValidator
        PY_OLD = PlacaParaguayAntigaValidator
