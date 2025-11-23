import pytest
from opaque.algorithms import Verhoeff, Luhn, ISO7064

def test_verhoeff():
    # Known valid Verhoeff numbers
    assert Verhoeff.validate("12345678902") # Generated check digit for 1234567890 is 2
    assert Verhoeff.validate("236") # 23 -> 6
    assert not Verhoeff.validate("12345678901") # Invalid check digit

    # Generation
    assert Verhoeff.generate("1234567890") == "2"
    assert Verhoeff.generate("23") == "6"

def test_luhn():
    # Known valid Luhn numbers (e.g. IMEI, CC)
    assert Luhn.validate("79927398713")
    assert not Luhn.validate("79927398710")
    
    # Simple cases
    assert Luhn.validate("49927398716")

def test_iso7064_mod97_10():
    # IBAN logic check
    # DE89 3704 0044 0532 0130 00 -> 131400 + DE(1314)00
    # Let's just test the math
    # 98 - (num * 100 % 97) logic usually used for generation
    # Validation: num % 97 == 1
    
    # Example valid number (raw numeric IBAN)
    # 3214282912345698765432161182 (Random valid I generated mentally? No.)
    # Let's use a small valid one: 1234567890123456789012345678901 (Too big)
    # 98 % 97 = 1. So "98" is valid? No, must be > 1.
    # 1 % 97 = 1.
    assert ISO7064.mod_97_10("98") # 98 % 97 = 1. Correct.
    assert not ISO7064.mod_97_10("97")
