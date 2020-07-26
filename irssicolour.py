#!/usr/bin/env python3

import sys

try:
	num = int(sys.argv[1])
except ValueError:
	print ( "argument must be a number" )
	exit(1)
except:
	print ( "Usage: {:s} <number>".format(sys.argv[0]) )
	exit(1)

if ( num < 0 or num > 255 ):
	print ( "number out of range" )
	exit(1)

if ( num < 17 ):
	print ( "{:02X}".format(num) )
	exit ( 0 )
else:
	num -=6

i=0
for section in range( 10, 257, 36 ):
	if ( num < section ):
		break
	i += 1

tens = i * 10
num -= (tens+((i-1)*26))

# if the remaining number is less than ten just use that
# if not, use str() to retrieve an ASCII char A-Z - kinda like hexadecimal
# but 36-based. Above 7x it's diferent again, here it's 0 == A. Bonkers.
if ( i < 7 ):
	if ( num < 10 ):
		ones = str(num)
	else:
		ones = chr((num-10)+65)
else:
	ones = chr(num+65)

# output
print ( "{}{:s}".format( int(tens/10), ones ) )	

exit ( 0 )

