fn main() {
    println!("Hello, world!");
    println!("Hello, world2!!!!!!!!!!!!!!");
    println!("{:.100}", add(1.1, 2.1));
    println!(
        "半径: {:.1}, 円周率: {:.100}, 面積: {:.3}",
        3.2,
        std::f64::consts::PI,
        3.2f64.powi(2) * std::f64::consts::PI,
    );
}

fn add(x: f64, y: f64) -> f64 {
    x + y
}
