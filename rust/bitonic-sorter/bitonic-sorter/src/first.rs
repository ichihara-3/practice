// pub　はこのsort関数が他のモジュールからアクセスできることを示す
// 引数xの型 &mut [u32] について
// &は値をポインタ経由で借用することを示す
// mutは可変であることを示す
// [u32]は32ビットの符号なし整数のスライス
pub fn sort(x: &mut [u32], up: bool) {
    if x.len() > 1 {
        let mid_point = x.len() / 2;
        sort(&mut x[..mid_point], true);
        sort(&mut x[mid_point..], false);
        sub_sort(x, up);
    }
}

fn sub_sort(x: &mut [u32], up: bool) {
    if x.len() > 1 {
        compare_and_swap(x, up);
        let mid_point = x.len() / 2;
        sub_sort(&mut x[..mid_point], up);
        sub_sort(&mut x[mid_point..], up);
    }
}

fn compare_and_swap(x: &mut [u32], up: bool) {
    let mid_point = x.len() / 2;
    for i in 0..mid_point {
        if (x[i] > x[mid_point + i]) == up {
            x.swap(i, mid_point + i)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::sort;

    #[test]
    fn sort_u32_ascending() {
        let mut x = vec![10, 30, 11, 20, 4, 330, 21, 110];
        sort(&mut x, true);
        assert_eq!(x, vec![4, 10, 11, 20, 21, 30, 110, 330]);
    }

    #[test]
    fn sort_u32_descending() {
        let mut x = vec![10, 30, 11, 20, 4, 330, 21, 110];
        sort(&mut x, false);
        assert_eq!(x, vec![330, 110, 30, 21, 20, 11, 10, 4]);
    }
}
