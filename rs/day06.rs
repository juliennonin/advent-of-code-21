fn update(counts: &mut [u64], days: u64, period: usize) {
    for _ in 0..days {
        // fish with an internal clock at 0 spawn
        // and their internal clock resets to 'period'
        counts[period] += counts[0];
        // decrease the internal clocks by one
        counts.rotate_left(1);
    }
}

fn main() {
    const PERIOD: usize = 7;
    const PERIOD_LONG: usize = PERIOD + 2;

    // counts[k] contains the number of fish whose internal clock is k
    let mut counts: [u64; PERIOD_LONG] = [0; PERIOD_LONG];
    include_str!("../data/day06.txt").trim().split(',')
        .map(|x| x.parse().unwrap())
        .for_each(|x:usize| counts[x] += 1);
    // counts = [0, 1, 1, 2, 1, 0, 0, 0, 0]; // Decomment for testing
    
    update(&mut counts, 80, PERIOD);
    println!("Part 1 — {:?}", counts.iter().sum::<u64>());
    update(&mut counts, 256 - 80, PERIOD);
    println!("Part 2 — {:?}", counts.iter().sum::<u64>());
}