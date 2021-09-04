fn print_message(name: &String) {
    println!("Hello, {}", name);
}

fn main() {
    let a = String::from("World");
    let b = &a;
    print_message(b);
    print_message(&a);
    println!("{}", a);
}
