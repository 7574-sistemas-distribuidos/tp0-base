package communication

import "fmt"

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
