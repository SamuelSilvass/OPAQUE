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
