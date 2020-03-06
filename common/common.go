package common

import (
	"fmt"
	"time"
)

func Example() {
	fmt.Sprintf("[COMMON] This function is executed in package common. Waiting 20 seconds for rabbit to come up...")
	time.Sleep(20 * time.Second)
	fmt.Sprintf("[COMMON] Done")
}
