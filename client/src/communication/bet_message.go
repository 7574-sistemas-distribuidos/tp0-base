package communication

import "fmt"

type BetMessage struct {
	Name      string
	LastName  string
	IdNumber  string
	Birthdate string
	BetNumber string
}

func (bm *(BetMessage)) Serialize() string {
	message := fmt.Sprintf("%s, %s, %s, %s, %s", bm.Name, bm.LastName, bm.IdNumber, bm.Birthdate, bm.BetNumber)
	return message
}
