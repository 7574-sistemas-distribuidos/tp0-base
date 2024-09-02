package communication

import (
	"fmt"
	"strings"
)

type BetContent struct {
	Name      string
	LastName  string
	IdNumber  string
	Birthdate string
	BetNumber string
}

func (bc *(BetContent)) Serialize() string {
	content := fmt.Sprintf("%s, %s, %s, %s, %s", bc.Name, bc.LastName, bc.IdNumber, bc.Birthdate, bc.BetNumber)
	return content
}

func DeserializeBetContent(content string) *BetContent {
	fields := strings.Split(content, ",")
	name := fields[0]
	lastName := fields[1]
	idNumber := fields[2]
	birthdate := fields[3]
	betNumber := fields[4]
	return &BetContent{Name: name, LastName: lastName, IdNumber: idNumber, Birthdate: birthdate, BetNumber: betNumber}
}
