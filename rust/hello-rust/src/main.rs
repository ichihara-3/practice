
struct Point {
    x: i32,
    y: i32,
}

fn get_point() -> Point {
    return Point {
        x: 0,
        y: 0,
    };
}


fn main() {
    let p = get_point();
    println!("{} {}", p.x, p.y);
}
