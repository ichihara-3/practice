// pub　はこのsort関数が他のモジュールからアクセスできることを示す
// 引数xの型 &mut [u32] について
// &は値をポインタ経由で借用することを示す
// mutは可変であることを示す
// [u32]は32ビットの符号なし整数のスライス
use super::SortOrder;
use std::cmp::Ordering;

pub fn sort<T: Ord>(x: &mut [T], order: &SortOrder) -> Result<(), String> {
    match *order {
        SortOrder::Ascending => sort_by(x, &|a, b| a.cmp(b)),
        SortOrder::Descending => sort_by(x, &|a, b| b.cmp(a)),
    }
}

pub fn sort_by<T, F>(x: &mut [T], comparator: &F) -> Result<(), String>
where
    F: Fn(&T, &T) -> Ordering,
{
    if x.len().is_power_of_two() {
        do_sort(x, true, comparator);
        Ok(())
    } else {
        Err(format!(
            "The length of x is not a power of two. (x.len(): {})",
            x.len()
        ))
    }
}

fn do_sort<T, F>(x: &mut [T], forward: bool, comparator: &F)
where
    F: Fn(&T, &T) -> Ordering,
{
    if x.len() > 1 {
        let mid_point = x.len() / 2;
        do_sort(&mut x[..mid_point], true, comparator);
        do_sort(&mut x[mid_point..], false, comparator);
        sub_sort(x, forward, comparator);
    }
}

fn sub_sort<T, F>(x: &mut [T], forward: bool, comparator: &F)
where
    F: Fn(&T, &T) -> Ordering,
{
    if x.len() > 1 {
        compare_and_swap(x, forward, comparator);
        let mid_point = x.len() / 2;
        sub_sort(&mut x[..mid_point], forward, comparator);
        sub_sort(&mut x[mid_point..], forward, comparator);
    }
}

fn compare_and_swap<T, F>(x: &mut [T], forward: bool, comparator: &F)
where
    F: Fn(&T, &T) -> Ordering,
{
    let swap_condition = if forward {
        Ordering::Greater
    } else {
        Ordering::Less
    };
    let mid_point = x.len() / 2;
    for i in 0..mid_point {
        if comparator(&x[i], &x[mid_point + i]) == swap_condition {
            x.swap(i, mid_point + i)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{sort, sort_by};
    use crate::SortOrder::*;
    use crate::utils::{new_u32_vec, is_sorted_ascending, is_sorted_descending};

    #[test]
    fn sort_u32_ascending() {
        let mut x: Vec<u32> = vec![10, 30, 11, 20, 4, 330, 21, 110];
        assert_eq!(sort(&mut x, &Ascending), Ok(()));
        assert_eq!(x, vec![4, 10, 11, 20, 21, 30, 110, 330]);
    }

    #[test]
    fn sort_u32_descending() {
        let mut x: Vec<u32> = vec![10, 30, 11, 20, 4, 330, 21, 110];
        assert_eq!(sort(&mut x, &Descending), Ok(()));
        assert_eq!(x, vec![330, 110, 30, 21, 20, 11, 10, 4]);
    }

    #[test]
    fn sort_str_descending() {
        let mut x = vec![
            "Rust",
            "is",
            "fast",
            "and",
            "memory-efficient",
            "with",
            "no",
            "GC",
        ];
        assert_eq!(sort(&mut x, &Descending), Ok(()));
        assert_eq!(
            x,
            vec![
                "with",
                "no",
                "memory-efficient",
                "is",
                "fast",
                "and",
                "Rust",
                "GC"
            ]
        );
    }

    #[test]
    fn sort_to_fail() {
        let mut x = vec![10, 30, 11];
        assert!(sort(&mut x, &Ascending).is_err());
    }

    #[derive(Debug, PartialEq)]
    struct Student {
        first_name: String,
        last_name: String,
        age: u8,
    }

    impl Student {
        fn new(first_name: &str, last_name: &str, age: u8) -> Self {
            Self {
                first_name: first_name.to_string(),
                last_name: last_name.to_string(),
                age,
            }
        }
    }

    #[test]
    fn sort_students_by_age_ascending() {
        let taro = Student::new("Taro", "Yamada", 16);
        let hanako = Student::new("Hanako", "Yamada", 14);
        let kyoko = Student::new("Kyoko", "Ito", 15);
        let ryosuke = Student::new("Ryosuke", "Hayashi", 17);
        let mut x = vec![&taro, &hanako, &kyoko, &ryosuke];
        let expected = vec![&hanako, &kyoko, &taro, &ryosuke];

        assert_eq!(sort_by(&mut x, &|a, b| a.age.cmp(&b.age)), Ok(()));

        assert_eq!(x, expected);
    }

    #[test]
    fn sort_students_by_name_ascending() {
        let taro = Student::new("Taro", "Yamada", 16);
        let hanako = Student::new("Hanako", "Yamada", 14);
        let kyoko = Student::new("Kyoko", "Ito", 15);
        let ryosuke = Student::new("Ryosuke", "Hayashi", 17);
        let mut x = vec![&taro, &hanako, &kyoko, &ryosuke];
        let expected = vec![&ryosuke, &kyoko, &hanako, &taro];

        assert_eq!(
            sort_by(&mut x, &|a, b| a
                .last_name
                .cmp(&b.last_name)
                .then_with(|| a.first_name.cmp(&b.first_name))),
            Ok(())
        );

        assert_eq!(x, expected);
    }
    
    #[test]
    fn sort_u32_large() {
        {
            let mut x = new_u32_vec(65536);
            assert_eq!(sort(&mut x, &Ascending), Ok(()));
            assert!(is_sorted_ascending(&x));
        }
        {
            let mut x = new_u32_vec(65536);
            assert_eq!(sort(&mut x, &Descending), Ok(()));
            assert!(is_sorted_descending(&x));
        }
    }
}
