package unionfind

import (
	"testing"
)

func TestUnionFind_Same(t *testing.T) {

	n := 10
	newu := NewUnionFind(n)

	newu.Unite(1, 2)

	var actual, expected bool

	actual = newu.Same(1, 2)
	expected = true
	if actual != expected {
		t.Errorf("len::\n\tgot: %v\n\twant:%v\n", actual, expected)
	}

	actual = newu.Same(1, 3)
	expected = false
	if actual != expected {
		t.Errorf("len::\n\tgot: %v\n\twant:%v\n", actual, expected)
	}
}

func TestUnionFind_Unite(t *testing.T) {

	n := 10
	newu := NewUnionFind(n)

	newu.Unite(1, 2)

	newu.Unite(2, 3)

	var actual, expected int

	actual = newu.Size(1)
	expected = 3
	if actual != expected {
		t.Errorf("size::\n\tgot: %v\n\twant:%v\n", actual, expected)
	}

	actual = newu.Root(1)
	expected = 3
	if actual != expected {
		t.Errorf("root::\n\tgot: %v\n\twant:%v\n", actual, expected)
	}

	newu.Unite(4, 5)
	actual = newu.Size(1)
	expected = 3
	if actual != expected {
		t.Errorf("size::\n\tgot: %v\n\twant:%v\n", actual, expected)
	}

	newu.Unite(1, 5)
	actual = newu.Size(1)
	expected = 5
	if actual != expected {
		t.Errorf("size::\n\tgot: %v\n\twant:%v\n", actual, expected)
	}
}
