package common

import (
    "encoding/binary"
)

type Bet struct {
	Id        int
	Name      string    
	LastName  string    
	Document  int       
	Birthdate string
	Number    int       
}

//  |- Id -|------ Name ------|------ LastName ------|- Document -|--  Birthdate --|- Number -|
//  |- 4b -|------  24b ------|------   24b    ------|-    4b    -|--    10b     --|-   4b   -|
func SerializeBet(bet Bet) []byte {
	buf := make([]byte, 0)

	// Id
	idBytes := make([]byte, 4) 
	binary.BigEndian.PutUint32(idBytes, uint32(bet.Id))

	// Name
	nameBytes := make([]byte, 24) 
	copy(nameBytes, []byte(bet.Name))

	// LastName
	lastNameBytes := make([]byte, 24) 
	copy(lastNameBytes, []byte(bet.LastName))

	// Document
	documentBytes := make([]byte, 4) 
	binary.BigEndian.PutUint32(documentBytes, uint32(bet.Document))

	// Birthdate
	birthdateBytes := make([]byte, 10) 
	copy(birthdateBytes, []byte(bet.Birthdate))

	// Number
	numberBytes := make([]byte, 4) 
	binary.BigEndian.PutUint32(numberBytes, uint32(bet.Number))

	buf = append(buf, idBytes...)
	buf = append(buf, nameBytes...)
	buf = append(buf, lastNameBytes...)
	buf = append(buf, documentBytes...)
	buf = append(buf, birthdateBytes...)
	buf = append(buf, numberBytes...)

	return buf
}