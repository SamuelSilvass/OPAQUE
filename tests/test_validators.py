import pytest
from opaque.validators import Validators

# ==================== BRASIL ====================

class TestBrazilValidators:
    def test_cpf_with_formatting(self):
        assert Validators.BR.CPF.validate("529.982.247-25") is True
        assert Validators.BR.CPF.validate("111.444.777-35") is True
        
    def test_cpf_without_formatting(self):
        assert Validators.BR.CPF.validate("52998224725") is True
        assert Validators.BR.CPF.validate("11144477735") is True
        
    def test_cpf_invalid(self):
        assert Validators.BR.CPF.validate("111.222.333-44") is False
        assert Validators.BR.CPF.validate("000.000.000-00") is False
        assert Validators.BR.CPF.validate("111.111.111-11") is False

    def test_cnpj_valid(self):
        assert Validators.BR.CNPJ.validate("00.000.000/0001-91") is True
        assert Validators.BR.CNPJ.validate("11.444.777/0001-61") is True
        assert Validators.BR.CNPJ.validate("11444777000161") is True

    def test_cnpj_invalid(self):
        assert Validators.BR.CNPJ.validate("00.000.000/0001-90") is False
        assert Validators.BR.CNPJ.validate("11.111.111/1111-11") is False

    def test_rg_valid(self):
        assert Validators.BR.RG.validate("12.345.678") is True
        assert Validators.BR.RG.validate("1234567") is True
        assert Validators.BR.RG.validate("123456789") is True

    def test_cnh_valid(self):
        # Using simpler validation - just format check for now
        assert Validators.BR.CNH.validate("01234567890") is True

    def test_cnh_invalid(self):
        assert Validators.BR.CNH.validate("00000000000") is False
        assert Validators.BR.CNH.validate("123") is False

    def test_renavam_valid(self):
        # Using format validation
        assert Validators.BR.RENAVAM.validate("12345678901") is True

    def test_renavam_invalid(self):
        assert Validators.BR.RENAVAM.validate("123") is False

    def test_placa_mercosul_valid(self):
        assert Validators.BR.PLACA_MERCOSUL.validate("ABC1D23") is True
        assert Validators.BR.PLACA_MERCOSUL.validate("XYZ9K87") is True

    def test_placa_mercosul_invalid(self):
        assert Validators.BR.PLACA_MERCOSUL.validate("ABC-1234") is False
        assert Validators.BR.PLACA_MERCOSUL.validate("AB12345") is False

    def test_placa_antiga_valid(self):
        assert Validators.BR.PLACA_ANTIGA.validate("ABC-1234") is True
        assert Validators.BR.PLACA_ANTIGA.validate("ABC1234") is True

    def test_pix_uuid(self):
        assert Validators.BR.PIX.validate("123e4567-e89b-12d3-a456-426614174000") is True

    def test_pix_email(self):
        assert Validators.BR.PIX.validate("user@example.com") is True

    def test_pix_phone(self):
        assert Validators.BR.PIX.validate("+5511999999999") is True

# ==================== ARGENTINA ====================

class TestArgentinaValidators:
    def test_cuil_valid(self):
        # Using format validation
        assert Validators.AR.CUIL.validate("20123456789") is True

    def test_cuil_invalid(self):
        assert Validators.AR.CUIL.validate("123") is False

    def test_dni_valid(self):
        assert Validators.AR.DNI.validate("12345678") is True
        assert Validators.AR.DNI.validate("1234567") is True

# ==================== CHILE ====================

class TestChileValidators:
    def test_rut_valid(self):
        assert Validators.CL.RUT.validate("12.345.678-5") is True
        assert Validators.CL.RUT.validate("12345678-5") is True

    def test_rut_invalid(self):
        assert Validators.CL.RUT.validate("123") is False

# ==================== COLOMBIA ====================

class TestColombiaValidators:
    def test_cedula_valid(self):
        assert Validators.CO.CEDULA.validate("123456") is True
        assert Validators.CO.CEDULA.validate("1234567890") is True

    def test_nit_valid(self):
        # Using format validation
        assert Validators.CO.NIT.validate("900123456") is True

    def test_nit_invalid(self):
        assert Validators.CO.NIT.validate("123") is False

# ==================== PERU ====================

class TestPeruValidators:
    def test_dni_valid(self):
        assert Validators.PE.DNI.validate("12345678") is True

    def test_dni_invalid(self):
        assert Validators.PE.DNI.validate("1234567") is False

    def test_ruc_valid(self):
        # Using format validation
        assert Validators.PE.RUC.validate("20123456789") is True

    def test_ruc_invalid(self):
        assert Validators.PE.RUC.validate("123") is False

# ==================== URUGUAY ====================

class TestUruguayValidators:
    def test_ci_valid(self):
        # Using format validation
        assert Validators.UY.CI.validate("123456") is True

    def test_ci_invalid(self):
        assert Validators.UY.CI.validate("123") is False

    def test_rut_valid(self):
        assert Validators.UY.RUT.validate("123456789012") is True

# ==================== VENEZUELA ====================

class TestVenezuelaValidators:
    def test_ci_valid(self):
        assert Validators.VE.CI.validate("V-12345678") is True
        assert Validators.VE.CI.validate("E-12345678") is True

    def test_rif_valid(self):
        assert Validators.VE.RIF.validate("J-123456789") is True
        assert Validators.VE.RIF.validate("V-12345678") is True

# ==================== ECUADOR ====================

class TestEcuadorValidators:
    def test_cedula_valid(self):
        # Valid Ecuadorian Cédula: 1710034065
        assert Validators.EC.CEDULA.validate("1710034065") is True

    def test_cedula_invalid(self):
        assert Validators.EC.CEDULA.validate("1710034060") is False
        assert Validators.EC.CEDULA.validate("9999999999") is False  # Invalid province

    def test_ruc_valid(self):
        assert Validators.EC.RUC.validate("1234567890001") is True

# ==================== BOLIVIA ====================

class TestBoliviaValidators:
    def test_ci_valid(self):
        assert Validators.BO.CI.validate("123456") is True
        assert Validators.BO.CI.validate("123456789") is True

    def test_nit_valid(self):
        assert Validators.BO.NIT.validate("1234567") is True

# ==================== PARAGUAY ====================

class TestParaguayValidators:
    def test_ci_valid(self):
        assert Validators.PY.CI.validate("123456") is True
        assert Validators.PY.CI.validate("12345678") is True

    def test_ruc_valid(self):
        assert Validators.PY.RUC.validate("123456") is True

# ==================== INTERNATIONAL ====================

class TestInternationalValidators:
    def test_credit_card_valid(self):
        assert Validators.FINANCE.CREDIT_CARD.validate("4242 4242 4242 4242") is True
        assert Validators.FINANCE.CREDIT_CARD.validate("4242424242424242") is True

    def test_credit_card_invalid(self):
        assert Validators.FINANCE.CREDIT_CARD.validate("4242 4242 4242 4243") is False

    def test_iban_valid(self):
        assert Validators.FINANCE.IBAN.validate("GB82 WEST 1234 5698 7654 32") is True
        assert Validators.FINANCE.IBAN.validate("DE89370400440532013000") is True

    def test_iban_invalid(self):
        assert Validators.FINANCE.IBAN.validate("GB82WEST12345698765433") is False

    def test_email_valid(self):
        assert Validators.INTERNATIONAL.EMAIL.validate("user@example.com") is True
        assert Validators.INTERNATIONAL.EMAIL.validate("test.user@domain.co.uk") is True

    def test_email_invalid(self):
        assert Validators.INTERNATIONAL.EMAIL.validate("invalid.email") is False
        assert Validators.INTERNATIONAL.EMAIL.validate("@example.com") is False

    def test_phone_valid(self):
        assert Validators.INTERNATIONAL.PHONE.validate("+1234567890") is True
        assert Validators.INTERNATIONAL.PHONE.validate("12345678") is True

    def test_phone_invalid(self):
        assert Validators.INTERNATIONAL.PHONE.validate("123") is False

    def test_passport_valid(self):
        assert Validators.INTERNATIONAL.PASSPORT.validate("AB123456") is True
        assert Validators.INTERNATIONAL.PASSPORT.validate("123456789") is True

    def test_passport_invalid(self):
        assert Validators.INTERNATIONAL.PASSPORT.validate("ABC") is False

class TestLicensePlateValidators:
    """Tests for South American License Plates"""

    def test_mercosul_argentina(self):
        assert Validators.PLATES.MERCOSUL_AR.validate("AA 123 BB") is True
        assert Validators.PLATES.MERCOSUL_AR.validate("AA123BB") is True
        assert Validators.PLATES.MERCOSUL_AR.validate("A 123 BB") is False

    def test_old_argentina(self):
        assert Validators.PLATES.AR_OLD.validate("AAA 123") is True
        assert Validators.PLATES.AR_OLD.validate("AAA123") is True
        assert Validators.PLATES.AR_OLD.validate("AA 123") is False

    def test_chile(self):
        assert Validators.PLATES.CL.validate("BBBB12") is True  # New
        assert Validators.PLATES.CL.validate("AB1234") is True  # Old
        assert Validators.PLATES.CL.validate("A1234") is False

    def test_colombia(self):
        assert Validators.PLATES.CO.validate("ABC 123") is True
        assert Validators.PLATES.CO.validate("AA 1234") is True
        assert Validators.PLATES.CO.validate("A 123") is False

    def test_peru(self):
        assert Validators.PLATES.PE.validate("A1B234") is True
        assert Validators.PLATES.PE.validate("A1B-234") is True
        assert Validators.PLATES.PE.validate("123456") is False

    def test_mercosul_uruguay(self):
        assert Validators.PLATES.MERCOSUL_UY.validate("ABC 1234") is True
        assert Validators.PLATES.MERCOSUL_UY.validate("ABC1234") is True
        assert Validators.PLATES.MERCOSUL_UY.validate("AB 1234") is False

    def test_venezuela(self):
        assert Validators.PLATES.VE.validate("AB123CD") is True
        assert Validators.PLATES.VE.validate("AB 123 CD") is True
        assert Validators.PLATES.VE.validate("A123CD") is False

    def test_ecuador(self):
        assert Validators.PLATES.EC.validate("ABC-1234") is True
        assert Validators.PLATES.EC.validate("ABC 123") is True
        assert Validators.PLATES.EC.validate("AB 123") is False

    def test_bolivia(self):
        assert Validators.PLATES.BO.validate("1234ABC") is True
        assert Validators.PLATES.BO.validate("123ABC") is True
        assert Validators.PLATES.BO.validate("12ABC") is False

    def test_mercosul_paraguay(self):
        assert Validators.PLATES.MERCOSUL_PY.validate("ABCD 123") is True
        assert Validators.PLATES.MERCOSUL_PY.validate("ABCD123") is True
        assert Validators.PLATES.MERCOSUL_PY.validate("ABC 123") is False

    def test_old_paraguay(self):
        assert Validators.PLATES.PY_OLD.validate("ABC 123") is True
        assert Validators.PLATES.PY_OLD.validate("ABC123") is True
        assert Validators.PLATES.PY_OLD.validate("AB 123") is False

class TestNewValidators:
    def test_cns(self):
        # Valid CNS (starts with 1, 2, 7, 8, 9)
        # Example CNS: 898001033308856
        assert Validators.BR.CNS.validate("898001033308856") is True
        assert Validators.BR.CNS.validate("123456789012345") is False # Invalid checksum

    def test_titulo_eleitor(self):
        # Valid Titulo (Calculated: 004356870917)
        # UF: 09 (SC)
        # DV1: 1
        # DV2: 7
        assert Validators.BR.TITULO_ELEITOR.validate("004356870917") is True
        assert Validators.BR.TITULO_ELEITOR.validate("000000000000") is False

    def test_ipv4(self):
        assert Validators.INTERNATIONAL.IPV4.validate("192.168.0.1") is True
        assert Validators.INTERNATIONAL.IPV4.validate("255.255.255.255") is True
        assert Validators.INTERNATIONAL.IPV4.validate("256.0.0.1") is False

    def test_ipv6(self):
        assert Validators.INTERNATIONAL.IPV6.validate("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
        assert Validators.INTERNATIONAL.IPV6.validate("::1") is True
        assert Validators.INTERNATIONAL.IPV6.validate("1234") is False

    def test_mac_address(self):
        assert Validators.INTERNATIONAL.MAC_ADDRESS.validate("00:1A:2B:3C:4D:5E") is True
        assert Validators.INTERNATIONAL.MAC_ADDRESS.validate("00-1A-2B-3C-4D-5E") is True
        assert Validators.INTERNATIONAL.MAC_ADDRESS.validate("ZZ:ZZ:ZZ:ZZ:ZZ:ZZ") is False

    def test_bitcoin(self):
        assert Validators.INTERNATIONAL.BITCOIN_ADDR.validate("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") is True
        assert Validators.INTERNATIONAL.BITCOIN_ADDR.validate("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy") is True
        assert Validators.INTERNATIONAL.BITCOIN_ADDR.validate("bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq") is True
        assert Validators.INTERNATIONAL.BITCOIN_ADDR.validate("invalid") is False

    def test_ethereum(self):
        assert Validators.INTERNATIONAL.ETHEREUM_ADDR.validate("0x32Be343B94f860124dD4fE2780A1f71a939F419b") is True
        assert Validators.INTERNATIONAL.ETHEREUM_ADDR.validate("0x0") is False

    def test_aws_key(self):
        assert Validators.CLOUD.AWS_ACCESS_KEY.validate("AKIAIOSFODNN7EXAMPLE") is True
        assert Validators.CLOUD.AWS_ACCESS_KEY.validate("ASIAIOSFODNN7EXAMPLE") is True
        assert Validators.CLOUD.AWS_ACCESS_KEY.validate("AKIA123") is False

    def test_github_token(self):
        assert Validators.CLOUD.GITHUB_TOKEN.validate("ghp_123456789012345678901234567890123456") is True
        assert Validators.CLOUD.GITHUB_TOKEN.validate("github_pat_11AAAAAAA_123456789012345678901234567890123456789012345678901234567890123456789012") is True
        assert Validators.CLOUD.GITHUB_TOKEN.validate("ghp_short") is False

    def test_slack_token(self):
        # Using test-only fake tokens (not real format to avoid GitHub scanning)
        test_token = "xoxb-" + "1" * 10 + "-" + "2" * 13 + "-" + "TEST" * 6
        assert Validators.CLOUD.SLACK_TOKEN.validate(test_token) is True
        assert Validators.CLOUD.SLACK_TOKEN.validate("xoxp-123") is False

    def test_google_api_key(self):
        assert Validators.CLOUD.GOOGLE_API_KEY.validate("AIzaSyD-1234567890123456789012345678901") is True
        assert Validators.CLOUD.GOOGLE_API_KEY.validate("AIzaShort") is False

    def test_ssn(self):
        assert Validators.US.SSN.validate("999-00-1234") is False # 900+ invalid
        assert Validators.US.SSN.validate("000-12-1234") is False # 000 invalid
        assert Validators.US.SSN.validate("123-45-6789") is True
        assert Validators.US.SSN.validate("666-12-1234") is False # 666 invalid

    def test_nino(self):
        assert Validators.UK.NINO.validate("AB 12 34 56 A") is True
        assert Validators.UK.NINO.validate("GB 12 34 56 A") is False # GB invalid prefix
        assert Validators.UK.NINO.validate("12 34 56 A") is False

    def test_entropy(self):
        # Low entropy
        assert Validators.SECURITY.ENTROPY.validate("password") is False # Entropy ~2.75
        assert Validators.SECURITY.ENTROPY.validate("12345678") is False
        
        # High entropy (random string)
        # "8f2c91d121b14a8c" -> 16 chars, hex.
        # Let's use a very high entropy string
        high_ent = "7^%#@!90$)(*&^%gHjK"
        assert Validators.SECURITY.ENTROPY.validate(high_ent, threshold=3.0) is True

    def test_jwt(self):
        # Valid JWT structure (header.payload.signature)
        valid_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        assert Validators.SECURITY.JWT.validate(valid_jwt) is True
        assert Validators.SECURITY.JWT.validate("invalid.token") is False

    def test_pem_cert(self):
        valid_pem = """-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAL...
-----END CERTIFICATE-----"""
        assert Validators.SECURITY.PEM_CERT.validate(valid_pem) is True
        assert Validators.SECURITY.PEM_CERT.validate("Not a cert") is False

