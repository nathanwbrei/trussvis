$(document).ready(function(){

    width = 600;
    height = 400;

    svg = d3.select("svg")
        .attr("viewBox", "0 0 " + width + " " + height )
        .attr("preserveAspectRatio", "xMidYMid meet");

    svg.selectAll(".background").on("click", function(d){
        var mouse = d3.mouse(this);
        var x = Math.round(xscale.invert(mouse[0])*1000)/1000;
        var y = Math.round(yscale.invert(mouse[1])*1000)/1000;

        controller2.typer.consoleInsert(" "+x+" "+y);
        console.log("click"+mouse);

        });
});


update_svg = function(members, interfaces){
    // Redo this with object constancy
    // http://mbostock.github.com/d3/tutorial/bar-2.html

    // xmin = d3.min(interfaces, function(d){return d['x'];});
    // xmax = d3.min(interfaces, function(d){return d['x'];});
    // ymin = d3.min(interfaces, function(d){return d['y'];});
    xmin = -10;
    xmax = 20;
    ymin = -5


    xscale = d3.scale.linear()
                .domain([xmin, xmax])
                .range([0, 600]);
    yscale = d3.scale.linear()
                .domain([ymin, 2/3*xmax+ymin])
                .range([400, 0]);

    svg = d3.select("svg");
    svg.selectAll("line").remove()
    svg.selectAll("circle").remove()

    svg.selectAll(".edge")
        .data(members)
        .enter()
        .append("line")
        .attr("class", "edge")
        .attr("stroke", function(d,i) {
            color = d["color"]
            if (color){
                return color;
            }
            else
                return "white";
        })
        .attr("x1", function(d, i) {
            return xscale(interfaces[d["i0"]]["x"]);
            })
        .attr("y1", function(d, i) {
            return yscale(interfaces[d["i0"]]["y"]);
            })
        .attr("x2", function(d, i) {
            return xscale(interfaces[d["i1"]]["x"]);
            })
        .attr("y2", function(d, i) {
            return yscale(interfaces[d["i1"]]["y"]);
            })
        .on("click", function(d) {
            controller2.typer.consoleInsert(" e"+d['mid']);
            })
        .on("mouseout", function(d) {d3.select(this).attr("stroke", d["color"] ? d["color"] : "white")})
        .on("mouseover", function() {d3.select(this).attr("stroke","red")});


    svg.selectAll(".node")
        .data(interfaces)
        .enter()
        .append("circle")
        .attr("class", "node")
        .attr("r", 5)
        .attr("cx", function(d, i) {
            return xscale(d["x"]);
            })
        .attr("cy", function(d, i) {
            return yscale(d["y"]);
            })
        .on("click", function(d) { 
            controller2.typer.consoleInsert(" n"+d['iid']);
            //d['iid']);
            })
        .on("mouseout", function(d) {d3.select(this).attr("class", "node deselected")})
        .on("mouseover", function() {d3.select(this).attr("class","node selected")});

    }
            