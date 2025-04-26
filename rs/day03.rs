fn majority_elmt(v: &Vec<u32>) -> Option<u32> {
    let mut m = 0;
    let mut i = 0;
    for elmt in v {
        if i == 0 {
            m = *elmt;
            i += 1;
        } else if m == *elmt {
            i += 1;
        } else {
            i -= 1;
        }
    }
    match i {
        0 => None,
        _ => Some(m),
    }
}

fn main() {
    let data: Vec<Vec<u32>> = include_str!("../data/day03.txt")
        .lines()
        .map(|line| line.chars().map(|x| x.to_digit(10).unwrap()).collect())
        .collect();


    let n = data[0].len() as u32;
    let mut eps = 0;
    let mut delta = 0;
    for i in 0..n {
        let col: Vec<u32> = data.iter().map(|v| v[i as usize]).collect();
        let bit = match majority_elmt(&col) {
            Some(m) => m,
            None => 1,
        };
        eps += bit * 2_u32.pow(n - i - 1);
        delta += (1 - bit) * 2_u32.pow(n - i - 1);
    }
    println!("{:?}", eps * delta);

}