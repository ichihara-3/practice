fn main() {
    // compile error
    {
        let a = String::from("Hello");
    }
    println!("{}, world!", a);
}

