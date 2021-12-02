
fn part1(course: &Vec<&str>) -> usize {
    let (mut h, mut d) = (0, 0);
    for line in course {
        let mut split = line.split_whitespace();
        let (direction, x): (&str, usize) = (split.next().unwrap(), split.next().unwrap().parse().unwrap());
        match direction {
            "forward" => {h += x},
            "down" => {d += x},
            "up" => {d -= x},
            _ => (),
        }
    }
    h * d
}

fn part2(course: &Vec<&str>) -> usize {
    let (mut h, mut d, mut aim) = (0, 0, 0);
    for line in course {
        let mut split = line.split_whitespace();
        let (direction, x): (&str, usize) = (split.next().unwrap(), split.next().unwrap().parse().unwrap());
        match direction {
            "forward" => {h += x; d += aim * x},
            "down" => {aim += x},
            "up" => {aim -= x},
            _ => (),
        }
    }
    h * d
}

fn main() {
    let course: Vec<&str> = include_str!("input.txt")
        .lines().collect();
    
    println!("Part 1 — {:?}", part1(&course));
    println!("Part 2 — {:?}", part2(&course));

}
