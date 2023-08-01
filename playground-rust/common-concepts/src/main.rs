use std::io;


fn array() {
    let a = [1, 2, 3, 4, 5];

    println!("Please input an index.");

    let mut index = String::new();

    io::stdin()
        .read_line(&mut index)
        .expect("Failed to read line");

    let index: usize = index.trim().parse().expect("Index entered was not a number");

    let element = a[index];

    println!(
        "The value of the element at index {} is: {}",
        index, element
    );
}

fn one_arg() {
    another_function(5);
}

fn another_function(x: i32) {
    println!("The value of x is: {}", x);
}

fn two_args() {
    another_function2(2, 'm');
}

fn another_function2(value: i32, unit_label: char) {
    println!{"The measurement is {value}{unit_label}"}
}

fn to_20() {
    let mut counter = 0;
    let result = loop {
        counter += 1;
        if counter == 10 {
            break counter * 2;
        }
    };
    
    println!("The result is {result}");
}

fn countdown() {
    let mut number = 3;
    while number != 0 {
        println!("{number}!");
        number -= 1;
    }
    println!("LIFTOFF!!!");
}

fn out_loud() {
    let a = [10, 20, 30, 40, 50];
    for element in a {
        println!("The value is: {element}");
    }
}

fn for_loop() {
    for number in (1..4).rev() {
        println!("{number}!");
    }
    println!("LIFTOFF!!!");
}

fn main() {
    println!("input a number n");
    let mut n = String::new();
    io::stdin()
        .read_line(&mut n)
        .expect("Failed to read line");
    let n: u32 = n.trim().parse().expect("n is not a number");
    println!("{}", fibo(n))
}

fn fibo(n: u32) -> u32 {
    if n == 0 {
        return 0;
    }
    if n == 1 {
        return 1;
    }
    else {
        return fibo(n-1) + fibo(n-2);
    }
}