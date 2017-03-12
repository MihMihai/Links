var font;
var vehicles = [];
var canvas;

function preload() {
    font = loadFont('js/Roboto-Black.ttf');
}

function windowResized() {
    clear();
    resizeCanvas(windowWidth, windowHeight);
    vehicles = [];
    var points = font.textToPoints('Links', width / 3.5, height / 1.5, width / 6

        , {
            sampleFactor: 0.2,
        }
        );

    for (var i = 0; i < points.length; i++) {
        var pt = points[i];
        var vehicle = new Vehicle(pt.x, pt.y);
        vehicles.push(vehicle);
        vehicles[i].pos = createVector(pt.x, pt.y);
    }
}

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.parent('canvas-holder');


    var points = font.textToPoints('Links', width / 3.5, height / 1.5, width / 6

        , {
            sampleFactor: 0.25
        }
        );

    for (var i = 0; i < points.length; i++) {
        var pt = points[i];
        var vehicle = new Vehicle(pt.x, pt.y);
        vehicles.push(vehicle);
    }
}

function draw() {

    background(color("#1D2026"));
    for (var i = 0; i < vehicles.length; i++) {
        var v = vehicles[i];
        v.behaviors();
        v.update();
        var green = map(i, 0, vehicles.length - 1, 100, 200);
        stroke(0, green, 0);
        v.show();
    }
}