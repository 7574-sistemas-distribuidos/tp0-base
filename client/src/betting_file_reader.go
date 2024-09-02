package common

import (
	"bufio"
	"os"
)

type BettingFileReader struct {
	file            *os.File
	bufferedScanner *bufio.Scanner
	eof             bool
	err             error
}

func NewBettingFileReader(filename string) (*BettingFileReader, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	return &BettingFileReader{file: file, bufferedScanner: bufio.NewScanner(file)}, nil
}

func (b *BettingFileReader) DeleteBettingFileReader() error {
	if b.file != nil {
		return b.file.Close()
	}
	return nil
}

func (b *BettingFileReader) ReadBet() string {
	ok := b.bufferedScanner.Scan()
	if !ok {
		if err := b.bufferedScanner.Err(); err != nil {
			b.err = err
			return ""
		}
		b.eof = true
	}
	return b.bufferedScanner.Text()
}

func (b *BettingFileReader) IsEOF() bool {
	return b.eof
}

func (b *BettingFileReader) Error() error {
	return b.err
}
