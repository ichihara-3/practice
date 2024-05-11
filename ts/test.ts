interface Point {
        x: number,
        y: number,
}

type Point3 = Point & {z: number}
interface Point3i extends Point { z: number}
        

function log(p: Point3i) {
        console.log(`x: ${p.x}`)
        console.log(`y: ${p.y}`)
        console.log(`z: ${p.z}`)
}


log({x: 1, y: 2, z: 3})

