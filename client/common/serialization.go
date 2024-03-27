package common

import (
	"fmt"
	"io"
	"encoding/csv"
    "encoding/binary"
	"strconv"
)

const RecordLen = 5
const maxBytes = 8 * 1024 

type Bet struct {
	Id        int
	Name      string    
	LastName  string    
	Document  int       
	Birthdate string
	Number    int       
}

func EncodeInt(id int) []byte {
	idBytes := make([]byte, 4) 
	binary.BigEndian.PutUint32(idBytes, uint32(id))
	return idBytes
}

//  |- Id -|------ Name ------|------ LastName ------|- Document -|--  Birthdate --|- Number -|
//  |- 4b -|------  24b ------|------   24b    ------|-    4b    -|--    10b     --|-   4b   -|
//  Total size = 4 + 24 + 24 + 4 + 10 + 4 = 70b
func SerializeBet(bet Bet) []byte {
	buf := make([]byte, 0)

	// Id
	idBytes := EncodeInt(bet.Id) 

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

func SerializeBets(bets []Bet) ([]byte, error) {
	chunkBets := make([]byte, 0)

	// Total bets to be received by the server
	betsLength := make([]byte, 4)
	binary.BigEndian.PutUint32(betsLength, uint32(len(bets)))
	chunkBets = append(chunkBets, betsLength...)

	// Serialize bets
	for _, bet := range bets {
		serializedBet := SerializeBet(bet)
		chunkBets = append(chunkBets, serializedBet...)
	}

	totalBytes := len(chunkBets)

	// Verify the maxbytes limit
	if totalBytes > maxBytes {
		return chunkBets, fmt.Errorf("Error the maximum size of bytes to be sent must not exceed 8kb")
	}

	return chunkBets, nil
}

// ProcessCSV reads bets from CSV reader and stores them in a list
// Returns the list of bets
func ProcessCSV(reader *csv.Reader, chunkSize int, id int) ([]Bet, error) {
	var bets []Bet

	for i := 0; i < chunkSize; i++ {
		record, err := reader.Read()
		if err != nil {
			if err == io.EOF {
				break
			}
			return nil, err
		}

		// Verificamos que tengamos suficientes campos en el registro
		if len(record) != RecordLen {
			return nil, fmt.Errorf("Error the record has less fields")
		}

		document, err := strconv.Atoi(record[2])
		if err != nil {
			return nil, fmt.Errorf("Error converting document to an integer: %v", err)
		}

		number, err := strconv.Atoi(record[4])
		if err != nil {
			return nil, fmt.Errorf("Error converting number to an integer %v", err)
		}

		// Crear una apuesta y agregarla a la lista de apuestas
		bet := Bet{
			Id:        id,
			Name:      record[0],
			LastName:  record[1],
			Document:  document,
			Birthdate: record[3],
			Number:    number,
		}
		bets = append(bets, bet)
	}

	return bets, nil
}