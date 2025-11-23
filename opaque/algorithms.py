"""
OPAQUE Mathematical Algorithms Module
=====================================

This module implements pure mathematical algorithms used for global document validation.
It includes advanced checksum algorithms like Verhoeff, ISO 7064, and optimized Luhn.
"""

from typing import List, Union

class Verhoeff:
    """
    The Verhoeff algorithm, a dihedral group D5 based checksum.
    Detects all single-digit errors and adjacent transposition errors.
    Used in: India (Aadhaar), Germany (Steuer-ID partial), etc.
    """
    
    # Multiplication table (D5)
    d = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]

    # Permutation table
    p = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]

    # Inverse table
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    @classmethod
    def validate(cls, num: Union[str, int]) -> bool:
        """Validates a number using Verhoeff checksum."""
        if not isinstance(num, str):
            num = str(num)
        
        if not num.isdigit():
            return False
            
        c = 0
        my_array = [int(x) for x in reversed(num)]
        
        for i, item in enumerate(my_array):
            c = cls.d[c][cls.p[i % 8][item]]
            
        return c == 0

    @classmethod
    def generate(cls, num: Union[str, int]) -> str:
        """Generates the Verhoeff checksum digit for a given number."""
        if not isinstance(num, str):
            num = str(num)
            
        c = 0
        my_array = [int(x) for x in reversed(num)]
        
        for i, item in enumerate(my_array):
            c = cls.d[c][cls.p[(i + 1) % 8][item]]
            
        return str(cls.inv[c])


class Luhn:
    """
    Optimized Luhn algorithm (Mod 10).
    Used in: Credit Cards, IMEI, NPI, Canadian SIN, etc.
    """
    @staticmethod
    def validate(num: Union[str, int]) -> bool:
        if not isinstance(num, str):
            num = str(num)
            
        if not num.isdigit():
            return False
            
        digits = [int(d) for d in num]
        checksum = 0
        reverse_digits = digits[::-1]
        
        for i, d in enumerate(reverse_digits):
            if i % 2 == 1:
                doubled = d * 2
                checksum += doubled if doubled < 10 else doubled - 9
            else:
                checksum += d
                
        return checksum % 10 == 0


class ISO7064:
    """
    ISO 7064 family of algorithms.
    """
    
    @staticmethod
    def mod_97_10(num: str) -> bool:
        """
        ISO 7064 Mod 97-10.
        Used in: IBAN, LEI (Legal Entity Identifier).
        """
        # Ensure numeric
        if not num.isdigit():
            return False
        return int(num) % 97 == 1

    @staticmethod
    def mod_11_2(num: str) -> bool:
        """
        ISO 7064 Mod 11-2.
        Used in: ORCID, CAS Registry Number.
        """
        # Implementation of pure ISO 11,2 if needed
        pass


class Mod11:
    """
    Generic Weighted Modulo 11 calculator.
    Used extensively in South American and Chinese documents.
    """
    @staticmethod
    def calculate_check_digit(digits: List[int], weights: List[int]) -> int:
        """Calculates standard Mod 11 check digit."""
        s = sum(d * w for d, w in zip(digits, weights))
        rem = s % 11
        if rem < 2:
            return 0
        return 11 - rem
