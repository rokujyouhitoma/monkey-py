let x = 5;
let y = 10;
let add = fn(a, b) {
    return a + b;
};
let multiply = fn(x) {
    return x * x;
}
let foobar = add(5, 5);
let barfoo = 5 * 5 / 10 + 18 - add(5, 5) + multiply(124);
let anotherName = barfoo;