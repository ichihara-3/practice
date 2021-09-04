
struct Point {
    x: i32,
    y: i32,
}

fn get_point<'a>() -> &'a Point {
    let p = Point {
        x: 0,
        y: 0,
    };
    &p
}


fn main() {
    let p = get_point();
    println!("{} {}", p.x, p.y);
}
