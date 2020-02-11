function greeter(person: string){
    return "Hello, " + person;
}

let User = "John Doe";
// let User = {Hello: 'world'};

document.body.textContent = greeter(User);
