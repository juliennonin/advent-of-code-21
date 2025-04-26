fn main() {
    let s: Vec<Vec<char>> = include_str!("../data/day09_test.txt").trim().split('\n').map(|line| line.chars().collect()).collect();
    let n = s.len();
    let m = s[0].len();
    for i in 0..2 {
        for j in 0..m {
            for (di, dj) in [(-1, 0), (1, 0), (0, -1 as isize), (0, 1)] {
                println!("{:?}, {:?}", i+di, j as isize+dj);
            }
        //     smallest = true;

        //     println!("{:?}", s[i][j]);
        }

    }
    println!("Hello world");
    println!("{:?}", s.len());
    // println!("{:?},{:?}", s[0][0], s[0][1]);
}