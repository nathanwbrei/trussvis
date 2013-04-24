
$(document).ready(function(){

    // We store our entire state/data model here.
    state = {"vis": {"nodes": [], "edges": []}, "geom": {"nodes": [], "edges": []}, "msg":"", "bcs": {"loadededges": [], "loadednodes": [], "fixednodes": []}}

    // Set up SVG to resize responsively. 
    // We can now pretend that SVG is always 600x400. 
    width = 600;
    height = 400;
    svg = d3.select("svg")
        .attr("viewBox", "0 0 " + width + " " + height )
        .attr("preserveAspectRatio", "xMinYMin meet");

    // Set scales, somehow. This needs to be redone.
    // xmin = d3.min(interfaces, function(d){return d['x'];});
    // xmax = d3.min(interfaces, function(d){return d['x'];});
    // ymin = d3.min(interfaces, function(d){return d['y'];});
    xmin = -10;
    xmax = 20;
    ymin = -5;
    xscale = d3.scale.linear()
                .domain([xmin, xmax])
                .range([0, 600]);
    yscale = d3.scale.linear()
                .domain([ymin, 2/3*xmax+ymin])
                .range([400, 0]);

    // Create background rectangle which responds to 
    // mouseclick by reporting coords. Used to create new nodes
    svg.selectAll(".background").on("click", function(d){
        var mouse = d3.mouse(this);
        var x = Math.round(xscale.invert(mouse[0])*1000)/1000;
        var y = Math.round(yscale.invert(mouse[1])*1000)/1000;

        controller2.typer.consoleInsert(" "+x+" "+y);
        });

    redraw()
    });

function redraw(){

    // Bind edge data to visualization via mID
    // Gives us object constancy -> nice animated transitions
    edges = svg.selectAll(".edge")
        .data(state['vis']['edges'], function(d){return d['mid']});

    // Enter function for edges.
    // Formats each incoming edge
    edges.enter()
        .insert("line")
        .attr("class", "edge")
        .attr("stroke", function(d,i) {
            color = d["color"]
            if (color){
                return color;
            }
            else
                return "gray";
        })
        .attr("x1", function(d, i) {
            return xscale(state['vis']['nodes'][d["i0"]]["x"]);
            })
        .attr("y1", function(d, i) {
            return yscale(state['vis']['nodes'][d["i0"]]["y"]);
            })
        .attr("x2", function(d, i) {
            return xscale(state['vis']['nodes'][d["i1"]]["x"]);
            })
        .attr("y2", function(d, i) {
            return yscale(state['vis']['nodes'][d["i1"]]["y"]);
            })
        .on("click", function(d) {
            controller2.typer.consoleInsert(" e"+d['mid']);
            })
        .on("mouseout", function(d) {d3.select(this).attr("stroke", d["color"] ? d["color"] : "gray")})
        .on("mouseover", function() {d3.select(this).attr("stroke","red")});

    // Nothing fancy for transitions or exits yet
    edges.transition().duration(500)
        .attr("stroke", function(d,i) {
            color = d["color"]
            if (color){
                return color;
            }
            else
                return "gray";
        })
        .attr("x1", function(d, i) {
            return xscale(state['vis']['nodes'][d["i0"]]["x"]);
            })
        .attr("y1", function(d, i) {
            return yscale(state['vis']['nodes'][d["i0"]]["y"]);
            })
        .attr("x2", function(d, i) {
            return xscale(state['vis']['nodes'][d["i1"]]["x"]);
            })
        .attr("y2", function(d, i) {
            return yscale(state['vis']['nodes'][d["i1"]]["y"]);
            });

    edges.exit().remove();

    // Bind node data to vis via iID
    // Gives us object constancy -> nice animated transitions 
    svg.selectAll(".node").remove();
    nodes = svg.selectAll(".node")
        .data(state['vis']['nodes'], function(d){return d['iid']});    

    nodes.enter()
        .insert("circle")
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
        .on("mouseout", function(d) {d3.select(this).attr("class", "node deselected");})
        .on("mouseover", function() {d3.select(this).attr("class","node selected");});
    nodes.transition().duration(500)
            .attr("cx", function(d, i) {
            return xscale(d["x"]);
            })
        .attr("cy", function(d, i) {
            return yscale(d["y"]);
            });

    nodes.exit().remove();
};


            
