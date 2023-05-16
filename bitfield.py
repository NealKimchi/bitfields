"""
A bit field is a range of binary digits within an
unsigned integer. Bit 0 is the low-order bit,
with value 1 = 2^0. Bit 31 is the high-order bit,
with value 2^31. 

A bitfield object is an aid to encoding and decoding 
instructions by packing and unpacking parts of the 
instruction in different fields within individual 
instruction words. 

Note that we are treating Python integers as if they 
were 32-bit unsigned integers.  They aren't ... Python 
actually uses a variable length signed integer
representation, but we ignore that because we are trying
to simulate a machine-level representation. 
"""

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

WORD_SIZE = 32 


class BitField(object):
    """A BitField object handles insertion and 
    extraction of one field within an integer.
    """
    def __init__(self, from_bit: int, to_bit: int) -> None:
        """Tool for  extracting bits 
            from_bit ... to_bit, where 0 is the low-order
            bit and 31 is the high-order bit of an unsigned
            32-bit integer. For example, the low-order 4 bits 
            could be represented by from_bit=0, to_bit=3. 
            """ 
        assert 0 <= from_bit < WORD_SIZE
        assert from_bit <= to_bit <= WORD_SIZE
        self.from_bit = from_bit
        self.to_bit = to_bit
        self.mask = 0
        for i in range(to_bit - from_bit + 1):
            self.mask = (self.mask << 1) | 1
        for i in range(from_bit):
            self.mask = self.mask << 1
        
    
    def extract(self, word: int) -> int:
        """Extract the bitfield and return it in the 
        low-order bits.  For example, if we are extracting
        bits 3..5, the result will be an 
        integer between 0 and 7 (0b000 to 0b111). 
        """
        result = self.mask & word
        return result >> self.from_bit
    
    def insert(self, value: int, word: int) -> int: 
        """Insert value, which should be in the low order 
            bits and no larger than the bitfield, into the 
            bitfield, which should be zero before insertion. 
            Returns the combined value. 
            Example: BitField(3,5).insert(0b101, 0b110) == 0b101110
            """
        value = value << self.from_bit
        value = value & self.mask
        return word | value
        
    
    def extract_signed(self, word: int) -> int:
        """Extract bits in bitfield as a signed integer."""
        extracted = self.extract(word)
        return sign_extend(extracted, self.to_bit - self.from_bit + 1)

def sign_extend(field: int, width: int) -> int:
    """Interpret field as a signed integer with width bits.
    If the sign bit is zero, it is positive.  If the sign bit
    is negative, the result is sign-extended to be a negative
    integer in Python.
    width must be 2 or greater. field must fit in width bits.
    """
    log.debug("Sign extending {} ({}) in field of {} bits".format(field, bin(field), width))
    assert width > 1
    assert field >= 0 and field < 1 << (width + 1)
    sign_bit = 1 << (width - 1) # will have form 1000... for width of field
    mask = sign_bit - 1         # will have form 0111... for width of field
    if (field & sign_bit):
        # It's negative; sign extend it
        log.debug("Complementing by subtracting 2^{}={}".format(width-1,sign_bit))
        extended = (field & mask) - sign_bit
        log.debug("Should return {} ({})".format(extended, bin(extended)))
        return extended
    else:
        return field


def main():
    pass

if __name__ == "__main__":
    main()

