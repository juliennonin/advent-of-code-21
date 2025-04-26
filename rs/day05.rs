// struct Line {
//     x1: usize,
//     y1: usize,
//     x2: usize,
//     y2: usize,
// }

fn main() {
    let data: Vec<&str> = include_str!("../data/day05_test.txt")
    .lines()
    // .map(|line| line.replace(" -> ", ",").split(',').collect())
    .collect();
    // .map(|line| line.chars().map(|x| x.to_digit(10).unwrap()).collect())
    // .collect();
    let _l = data[0];
    // let _line = l.replace(" -> ", ",").to_string(); //.split(',').collect();
    // let _line:Vec<&str> = line.split(',').collect();
    let a = "3,3 -> 5,15".replace(" -> ", ",").split(',');
    
    println!("{:?}", a);
}