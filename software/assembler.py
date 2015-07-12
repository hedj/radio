#!/usr/bin/python

# Generate a bitstream which when loaded by the GA144s SPI node will
# cause the SPI clock pin to toggle at approximately 1 Hz

# John Hedditch, 2015


## INSTRUCTION SET ##
## (See http://www.greenarraychips.com/home/documents/greg/DB001-110412-F18A.pdf)
  
blinky_program ="""

"""

class InstructionSet:
  table = {
    #    -- Control transfer --
    # mnemonic:  (op,     description)
    ";"        : (0x00,  "Return"),
    "ex"       : (0x01,  "Execute"),
    "name;"    : (0x02,  "Jump"),
    "name"     : (0x03,  "Call"),
    "unext"    : (0x04,  "Micronext"),
    "next"     : (0x05,  "Next"),
    "if"       : (0x06,  "If"),
    "-if"      : (0x07,  "Minus-If"),

    #    -- Memory ops --
    # mnemonic:  (op,     description)
    "@p"      :  (0x08,   "Fetch-P"),
    "@+"      :  (0x09,   "Fetch-plus"),
    "@b"      :  (0x0A,   "Fetch-B"),
    "@"       :  (0x0B,   "Fetch"),
    "!p"      :  (0x0C,   "Store-P"),
    "!+"      :  (0x0D,   "Store-plus"),
    "!b"      :  (0x0E,   "Store-B"),
    "!"       :  (0x0F,   "Store"),

    #    -- ALU and Register ops --
    # mnemonic:  (op,     description)
    "+*"      :  (0x10,   "Multiply step"),
    "2*"      :  (0x11,   "Two-Star (shift left 1 bit)"),
    "2/"      :  (0x12,   "Two-Slash (shift right 1 bit)"),
    "-"       :  (0x13,   "Not (Invert)"), 
    "+"       :  (0x14,   "Plus"),
    "and"     :  (0x15,   "T <- (S & T)"),
    "or"      :  (0x16,   "Exclusive Or"),
    "drop"    :  (0x17,   "Drop"),
    "dup"     :  (0x18,   "Duplicate top stack item"),
    "pop"     :  (0x19,   "Moves R into T, pops R"),
    "over"    :  (0x1A,   "Puts a copy of S on top of stack"),
    "a"       :  (0x1B,   "Pushes contents of A onto stack"),
    "."       :  (0x1C,   "Nop"),
    "push"    :  (0x1D,   "Pop T, push R"),
    "b!"      :  (0x1E,   "Pop T into register B"),
    "a!"      :  (0x1E,   "Pop T into register A"),
  }

  def __init__(self):
    pass
 
  def names(self):
    return self.table.keys() 

  def op(self,name):
    return self.table[name]

  def opcode(self, name):
    (code, _) = self.op(name)
    return code

  # only instructions with the two lowest-order
  # bits equal to zero can go in slot 4
  def allowedInSlotFour(self, name):
    return (self.opcode(name) & 0x11) == 0

  def assemble(self, instruction, slot):
    if (slot==4):
      if (self.allowedInSlotFour(instruction)):
        # return success, and the binary representation of the op
        return (True,  '{0:03b}'.format( self.opcode(instruction) >>2 ) ) 
      else:
        # return failure, and a binary nop 
        return (False, '{0:03b}'.format( self.opcode(".") >> 2 ) ) 
    else:
      return (True, '{0:05b}'.format( self.opcode(instruction) ) )
      
