
fn nb_increases(depths: &Vec<usize>, shift: usize) -> usize {
    depths.iter()
        .zip(depths.iter().skip(shift))
        .filter(|(a, b)| b > a).count()
}

fn main() {
    let depths: Vec<usize> = include_str!("../data/day01.txt")
        .lines()
        .map(|x| x.parse().unwrap()) // filter_map(|x| x.unwrap().parse().ok())
        .collect();
    // let depths: Vec<usize> = vec![1, 2, 3, 7, 5, 8];
    println!("Part 1 — {:?}", nb_increases(&depths, 1));
    println!("Part 2 — {:?}", nb_increases(&depths, 3));
}
