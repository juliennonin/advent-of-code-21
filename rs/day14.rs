use std::collections::HashMap;
use std::fmt;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Pair (char, char);

impl Pair {
    fn from_str(s: &str) -> Self {
        let char_vec: Vec<char> = s.chars().collect();
        Self(char_vec[0], char_vec[1])
    }

    fn insert(&self, elmt: char) -> (Self, Self) {
        (Self(self.0, elmt), Self(elmt, self.1))
    }
}

impl fmt::Display for Pair {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "'{}{}'", self.0, self.1)
    }
}
impl fmt::Debug for Pair {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "'{}{}'", self.0, self.1)
    }
}

//
fn polymer_to_pairs(polymer: &str) -> HashMap<Pair, usize> {
    let mut counts = HashMap::<Pair, usize>::new();
    for i in 0..(polymer.len() - 1) {
        *counts.entry(Pair::from_str(&polymer[i..i+2])).or_insert(0) += 1;
    }
    counts
}

fn count_elements(pairs: &HashMap<Pair, usize>, first: char) ->  HashMap<char, usize> {
    let mut counts = HashMap::<char, usize>::new();
    counts.insert(first, 1);
    for (pair, k) in pairs {
        *counts.entry(pair.1).or_insert(0) += k;
    }
    counts
}

// 
fn polymerize_once(pairs: &HashMap<Pair, usize>, templates: &HashMap<Pair, char>) -> HashMap<Pair, usize> {
    let mut pairs_new = pairs.clone();
    
    for (pair, k) in pairs {
        match templates.get(pair) {
            Some(elmt) => {
                let (pair1, pair2) = pair.insert(*elmt);
                *pairs_new.entry(pair1).or_insert(0) += *k;
                *pairs_new.entry(pair2).or_insert(0) += *k;
                *pairs_new.entry(*pair).or_insert(0) -= *k;
            },
            None => (),
        }
    }
    pairs_new
}

fn result(polymer: &str, n: usize, templates: &HashMap<Pair, char>) -> usize {
    let mut pairs = polymer_to_pairs(polymer);
    let first = polymer.chars().next().unwrap();
    for _ in 0..n {
        pairs = polymerize_once(&pairs, templates);
    }
    let counts = count_elements(&pairs, first);
    let counts_max = counts.iter().map(|(_k, v)| v).max().unwrap();
    let counts_min = counts.iter().map(|(_k, v)| v).min().unwrap();
    counts_max - counts_min
}

//
fn main() {
    let (polymer, templates) = include_str!("../data/day14.txt")
        .trim().split_once("\n\n").unwrap();
    let templates: HashMap<Pair, char> = templates.split("\n")
        .map(|tpl| tpl.split_once(" -> ").unwrap())
        .map(|(x, y)| (Pair::from_str(x), y.chars().collect::<Vec<char>>()[0]))
        .collect();

    let part1 = result(polymer, 10, &templates);
    let part2 = result(polymer, 40, &templates);

    println!("Part 1 — {}", part1);
    println!("Part 1 — {}", part2);
}
