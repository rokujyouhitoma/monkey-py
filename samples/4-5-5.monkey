let people = [{"name": "Alice", "age": 24}, {"name": "Anna", "age": 28}];
people[0]["name"];
people[1]["age"];
people[1]["age"] + people[0]["age"];
let getName = fn(person) { person["name"]; };
getName(people[0]);
getName(people[1]);
