
fn part1(course: &Vec<(&str, usize)>) -> usize {
    let (mut h, mut d) = (0, 0);
    for (direction, x) in course {
        match *direction {
            "forward" => h += x,
            "down" => d += x,
            "up" => d -= x,
            _ => (),
        }
    }
    h * d
}

fn part2(course: &Vec<(&str, usize)>) -> usize {
    let (mut h, mut d, mut aim) = (0, 0, 0);
    for (direction, x) in course {
        match *direction {
            "forward" => {h += x; d += aim * x},
            "down" => aim += x,
            "up" => aim -= x,
            _ => (),
        }
    }
    h * d
}

fn main() {
    let course: Vec<(&str, usize)> = include_str!("input.txt")
        .lines()
        .map(|line| line.split_once(" ").unwrap())
        .map(|line| (line.0, line.1.parse().unwrap()))
        .collect();
    
    println!("Part 1 — {:?}", part1(&course));
    println!("Part 2 — {:?}", part2(&course));

}
