use std::collections::HashSet;

#[derive(Hash, Eq, PartialEq, Debug)]
struct Coord (i16, i16);

impl Coord {
    fn from_str(s: &str) -> Self {
        let (x, y) = s.split_once(',').unwrap();
        let x: i16 = x.parse().unwrap();
        let y: i16 = y.parse().unwrap();
        Self(x, y)
    }

    fn symmetric_along_axis(&self, fold: &Fold) -> Self {
        match fold {
            Fold::Left(pos) if self.0 > *pos => Self(2 * pos - self.0, self.1),
            Fold::Up(pos) if self.1 > *pos => Self(self.0, 2 * pos - self.1),
            _ => Self(self.0, self.1)
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Fold {
    Up(i16),
    Left(i16),
}

impl Fold {
    fn from_str(s: &str) -> Self {
        let (xy, pos) = s.strip_prefix("fold along ")
            .unwrap().split_once("=").unwrap();
        let pos = pos.parse().unwrap();
        match xy {
            "x" => Self::Left(pos),
            "y" => Self::Up(pos),
            other => panic!("Must be either 'x' or 'y' but not {:?}", other)
        }
    }
}

fn represent_paper(paper: &HashSet<Coord>) -> String {
    let n_col = paper.iter().map(|coord| coord.0).max().unwrap() + 1;
    let n_row = paper.iter().map(|coord| coord.1).max().unwrap() + 1;
    (0..n_row).map(|j|
        (0..n_col).map(|i|
            if paper.contains(&Coord(i, j)) {"█"} else {" "}
        ).collect()).collect::<Vec<String>>().join("\n")
}

fn fold_paper(paper: &HashSet<Coord>, fold: &Fold) -> HashSet<Coord> {
    paper.iter().map(|c| c.symmetric_along_axis(fold)).collect()
}

fn main() {
    let (data_dots, instructions) = include_str!("../data/day13.txt")
        .trim().split_once("\n\n").unwrap();
    let mut data_dots: HashSet<Coord> = data_dots.split("\n")
        .map(Coord::from_str).collect();
    let instructions: Vec<Fold> = instructions.split("\n")
        .map(Fold::from_str).collect();

    let part1 = fold_paper(&data_dots, &instructions[0]).len();
    
    for fold in instructions {
        data_dots = fold_paper(&data_dots, &fold);
    }
    let part2 = represent_paper(&data_dots);

    println!("Part 1 — {}", part1);
    println!("Part 2 —\n{}", part2);
}
