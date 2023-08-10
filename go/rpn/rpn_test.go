package rpn

import (
	"testing"
)

func TestRpn(t *testing.T) {
	// case 1: "1 2 + 4 * 3 +" -> result: 15
	// case 2: "1 2 3 * + 4 +" -> result: 11
	// case 3: "1 2 3 4 + * +" -> result: 15
	// case 4: "1 2 3 4 + + *" -> result: 9
	// case 5: "1 2 3 * + 4 6 * +" -> result: 31
	// case 6: "3 4 2 * 1 5 - / +" -> result: 1
	testCases := []struct {
		input  string
		result int
	}{
		{"1 2 + 4 * 3 +", 15},
		{"1 2 3 * + 4 +", 11},
		{"1 2 3 4 + * +", 15},
		{"1 2 3 4 + + *", 9},
		{"1 2 3 * + 4 6 * +", 31},
		{"3 4 2 * 1 5 - / +", 1},
	}
	for _, tc := range testCases {
		result := rpn(tc.input)
		if result != tc.result {
			t.Errorf("rpn(%s) = %d, want %d", tc.input, result, tc.result)
		}
	}
}
