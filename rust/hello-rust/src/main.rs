fn main() {
    let a = String::from("Hello");
    let b = &a;
    println!("{}, world!", b);
    println!("{}, world!", a);
}
