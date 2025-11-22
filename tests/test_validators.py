import pytest
from opaque.validators import Validators

class TestCPFValidator:
    def test_valid_cpf(self):
        # Known valid CPFs
        assert Validators.BR.CPF.validate("529.982.247-25") is True
        assert Validators.BR.CPF.validate("111.444.777-35") is True
        
    def test_invalid_cpf_digits(self):
        # Invalid checksums
        assert Validators.BR.CPF.validate("111.222.333-44") is False
        assert Validators.BR.CPF.validate("123.456.789-00") is False

    def test_invalid_cpf_format(self):
        # Wrong length
        assert Validators.BR.CPF.validate("123.456.789") is False # Missing digits
        assert Validators.BR.CPF.validate("123.456.789-1") is False # Short
        
    def test_known_invalid_cpfs(self):
        # All digits equal are invalid despite passing math in some naive implementations
        # My implementation checks len(set(cpf)) == 1
        assert Validators.BR.CPF.validate("000.000.000-00") is False
        assert Validators.BR.CPF.validate("111.111.111-11") is False
        assert Validators.BR.CPF.validate("999.999.999-99") is False

class TestCNPJValidator:
    def test_valid_cnpj(self):
        # Banco do Brasil
        assert Validators.BR.CNPJ.validate("00.000.000/0001-91") is True
        # Google Brasil (approximate or random valid)
        # Let's use a generated valid one to be sure: 11.444.777/0001-61
        assert Validators.BR.CNPJ.validate("11.444.777/0001-61") is True

    def test_invalid_cnpj(self):
        assert Validators.BR.CNPJ.validate("00.000.000/0001-90") is False
        assert Validators.BR.CNPJ.validate("11.111.111/1111-11") is False

class TestCreditCardValidator:
    def test_valid_visa(self):
        # Stripe test card
        assert Validators.FINANCE.CREDIT_CARD.validate("4242 4242 4242 4242") is True
    
    def test_invalid_card(self):
        assert Validators.FINANCE.CREDIT_CARD.validate("4242 4242 4242 4243") is False

class TestPixValidator:
    def test_valid_uuid(self):
        assert Validators.BR.PIX.validate("123e4567-e89b-12d3-a456-426614174000") is True
        
    def test_valid_email(self):
        assert Validators.BR.PIX.validate("user@example.com") is True
        assert Validators.BR.PIX.validate("nome.sobrenome@empresa.com.br") is True
        
    def test_valid_phone(self):
        assert Validators.BR.PIX.validate("+5511999999999") is True
        
    def test_invalid_pix(self):
        assert Validators.BR.PIX.validate("not-a-pix-key") is False
        assert Validators.BR.PIX.validate("123") is False
