use std::cmp;

fn cost_part1(h: &Vec<isize>, pos: isize) -> usize {
    h.iter().map(|x| (*x - pos).abs() as usize).sum()
}

fn cost_part2(h: &Vec<isize>, pos: isize) -> usize {
    h.iter()
    .map(|x| (x - pos).pow(2) + (*x - pos).abs())
    .map(|c| (c / 2) as usize)
    .sum()
}

fn main() {
    let h: Vec<isize> = include_str!("../data/day07.txt")
        .trim().split(',')
        .map(|x| x.parse().unwrap()).collect();
    let n = h.len() as isize;
    

    let part1 = (1..n).map(|d| cost_part1(&h, d)).min().unwrap();
    // let part2 = (1..n).map(|d| cost_part2(&h, d)).min().unwrap();
    
    // analytical solutions
    let mean = h.iter().sum::<isize>() / n;
    let part2 = cmp::min(cost_part2(&h, mean), cost_part2(&h, mean + 1));

    println!("Part 1 — {:?}", part1);
    println!("Part 2 — {:?}", part2);
}