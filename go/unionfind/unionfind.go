package unionfind

type UnionFind struct {
	roots []int
	sizes []int
	ranks []int
}

func NewUnionFind(n int) UnionFind {
	roots := make([]int, n)
	sizes := make([]int, n)
	ranks := make([]int, n)
	for i := 0; i < n; i++ {
		roots[i] = i
		sizes[i] = 1
		ranks[i] = 1
	}
	return UnionFind{roots, sizes, ranks}
}

func (u *UnionFind) Root(x int) int {
	if u.roots[x] == x {
		return x
	}
	u.roots[x] = u.Root(u.roots[x])
	return u.roots[x]
}

func (u *UnionFind) Unite(x, y int) {
	x = u.Root(x)
	y = u.Root(y)

	if u.Same(x, y) {
		return
	}

	if u.Rank(x) > u.Rank(y) {
		x, y = y, x
	}

	u.sizes[x] += u.Size(y)

	u.roots[y] = x
	if u.Rank(x) == u.Rank(y) {
		u.ranks[x]++
	}
}

func (u *UnionFind) Rank(x int) int {
	return u.ranks[u.Root(x)]
}

func (u *UnionFind) Size(x int) int {
	return u.sizes[u.Root(x)]
}

func (u *UnionFind) Same(x, y int) bool {
	if u.Root(x) == u.Root(y) {
		return true
	}
	return false
}
