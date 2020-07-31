package main

import "fmt"
import "flag"
import "strconv"
import "os"

type ConvFunc func(int) string

var conv ConvFunc

func main() {
	irssi := flag.Bool("i", true, "Print irssi %xNN palette")
	palette256 := flag.Bool("n", false, "Print colourN palette")
	flag.Parse()

	if flag.NArg() > 0 {
		num, _ := strconv.Atoi(flag.Args()[0])
		if -1 < num && num < 256 {
			fmt.Println(convert(num))
		} else {
			fmt.Println("Argument ", num, " out of range")
			os.Exit(1)
		}
	} else {
		if *palette256 == true {
			conv = pass
		} else if *irssi == true {
			conv = convert
		}
		palette()
	}
}

func palette() {
	fg := 15
	for col := 0; col < 17; col++ {
		fmt.Print(printField(fg, col))
		fg = 0
	}
	fmt.Println("\x1B[93;65m\n")

	for _, hblock := range []int{16, 124} {
		for line := hblock; line < hblock+6*6; line += 6 {
			linechar := ""
			switch line {
			case 16, 124:
				fg = 15
			case 34, 142:
				fg = 0
			}
			for block := 0; block < 18; block += 6 {
				blockstart := block*6 + line
				for num := blockstart; num < blockstart+6; num++ {
					linechar += printField(fg, num)
				}
				linechar += "  "
			}
			fmt.Println(linechar)
		}
		fmt.Println()
	}
	fg = 15
	linechar := ""
	for greyscale := 232; greyscale < 256; greyscale++ {
		linechar += printField(fg, greyscale)
		if greyscale == 243 {
			linechar += "\n"
			fg = 0
		}
	}
	fmt.Print(linechar, "\n")
}

func printField(fg int, num int) string {
	return fmt.Sprintf("\x1B[38;5;%dm\x1B[48;5;%dm %s\x1B[48;5;0m", fg, num, conv(num))

}

func pass(num int) string {
	return fmt.Sprintf("%3d", num)
}

func convert(num int) string {
	if num < 17 {
		return fmt.Sprintf("%02X ", num)
	}
	num -= 6

	i := 1
	for section := 46; section < 257; section += 36 {
		if num < section {
			break
		}
		i++
	}

	tens := i * 10
	num -= (tens + ((i - 1) * 26))

	ones := ""
	if i < 7 {
		if num < 10 {
			ones = strconv.Itoa(num)
		} else {
			ones = string((num - 10) + 65)
		}
	} else {
		ones = string(num + 65)
	}
	return fmt.Sprintf("%d%s ", tens/10, ones)
}
