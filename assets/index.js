import p5 from 'p5';
// import $ from 'jquery';
// This draws p5.
const sketch = (s) => {
    let max_distance;
    let canvasDiv;
    let width;
    let height;
    console.log("hi");
    s.setup = () => {
        canvasDiv = document.getElementById('p5');
        width = canvasDiv.offsetWidth;
        height = canvasDiv.offsetHeight;
        let sketchCanvas = s.createCanvas(width, height);
        sketchCanvas.parent('p5');
        s.noStroke();
        max_distance = s.dist(0, 0, width, height);
    }
    s.draw = () => {
        s.background(240);
        for (let i=0; i <= width; i+= 30) {
            for (let j=0; j <= height; j+= 30) {
                let size = s.dist(s.mouseX, s.mouseY, i, j);
                size = (size / max_distance) * 80;
                // fill(150)
                s.ellipse(i, j, size, size);
            }
        }
    }
    s.windowResized = () => {
        canvasDiv = document.getElementById('p5');
        width = canvasDiv.offsetWidth;
        height = canvasDiv.offsetHeight;
        s.resizeCanvas(width, height);
    }
}

let nav = document.getElementById('navlist');
nav.style.transition = "all 200ms"
window.addEventListener("resize", () => {
    if (screen.width > 500 ) {
        nav.style.display = "";
    }
});
document.getElementById('toggle-nav').addEventListener("click", () => {
    nav = document.getElementById('navlist');
    if (nav.style.display === "") {
        nav.style.display = "block";
    } else {
        nav.style.display = "";
    }
});



// const sketchInstance = new p5(sketch);

// $(function() {
//     let contentCol = $('#content-col');
//     $('.swipeaway').click(function(e) {

//         let url = $(this).attr('href');
//         $("content").fadeOut(500, function() {
//             window.location = url;
//         })
//     });
// })