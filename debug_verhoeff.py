from opaque.algorithms import Verhoeff

base = "12345678901"
check = Verhoeff.generate(base)
full = base + check
print(f"Base: {base}")
print(f"Check: {check}")
print(f"Full: {full}")
print(f"Valid? {Verhoeff.validate(full)}")
