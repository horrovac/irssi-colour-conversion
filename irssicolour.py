#!/usr/bin/env python3

import sys

def main():
	try:
		num = int(sys.argv[1])
	except ValueError:
		print ( "argument must be a number" )
		exit(1)
	except:
		print_palette()
		exit(0)
		#print ( "Usage: {:s} <number>".format(sys.argv[0]) )
	
	if ( num < 0 or num > 255 ):
		print ( "number out of range (0-255)" )
		exit(1)

	print ( cvrt(num) )

def cvrt(num):
	if ( num < 17 ):
		return ( "{:02X}".format(num) )
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

	return "{}{:s}".format( int(tens/10), ones ) 


def print_palette():
	fg = 15
	linechar = ""
	for col16 in range ( 0, 16 ):
		linechar += "\x1B[38;5;{:d}m\x1B[48;5;{:d}m{:^4s}\x1B[48;5;0m".format(fg, col16, cvrt(col16)) 
		fg = 0
	
	print ( linechar + "\n" )	
	
	for hblock in [16, 124]:
		for line in range(hblock, hblock+6*6, 6):
			linechar = ""
			if ( line == 16 or line == 124 ):
				fg = 15
			elif ( line == 34 or line == 142 ):
				fg = 0
			for block in range ( 0, 18, 6 ):
				blockstart = block * 6 + line
				for num in range ( blockstart, blockstart+6 ):
					linechar += "\x1B[38;5;{:d}m\x1B[48;5;{:d}m{:^4s}\x1B[48;5;0m".format(fg, num, cvrt(num)) 
		
				linechar += "  "
			
			print ( linechar )
		print ( "" )
	
	
	fg = 15
	linechar = ""
	for greyscale in range ( 232, 256 ):
		linechar += "\x1B[38;5;{:d}m\x1B[48;5;{:d}m{:^4s}\x1B[48;5;0m".format(fg, greyscale, cvrt(greyscale)) 
		if ( greyscale == 243 ):
			linechar += "\n"
			fg = 0
	
	print ( linechar )

main()
