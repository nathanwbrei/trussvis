
$(document).ready(function(){

    // Make our modebar live
    d3.selectAll("#modebox li").on("click",function(d) { changemode(this.id)});
    mode = "geom";

    // We store our entire state/data model here.
    state = {"vis": {"nodes": [], "edges": []}, "geom": {"nodes": [], "edges": []}, "msg":"Welcome to TrussVis!", "bcs": {"loadededges": [], "loadednodes": [], "fixednodes": []}}

    // Set up SVG to resize responsively. 
    // We can now pretend that SVG is always 600x400. 
    width = 1200;
    height = 800;
    svg = d3.select("svg")
        .attr("viewBox", "0 0 " + width + " " + height )
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("class", "axis")

    // Set scales, somehow. This needs to be redone.
    // xmin = d3.min(interfaces, function(d){return d['x'];});
    // xmax = d3.min(interfaces, function(d){return d['x'];});
    // ymin = d3.min(interfaces, function(d){return d['y'];});
    xmin = -20;
    xmax = 40;
    ymin = -10;
    xscale = d3.scale.linear()
                .domain([xmin, xmax])
                .range([0, width]);
    yscale = d3.scale.linear()
                .domain([ymin, 2/3*xmax+ymin])
                .range([height, 0]);
    xaxis = d3.svg.axis().scale(xscale).ticks(10).orient("down");
    yaxis = d3.svg.axis().scale(yscale).ticks(8).orient("right");

    svg.append("svg:g")
              .attr("class", "x axis")
              .attr("transform", "translate(0, 500)")
              .call(xaxis);
    svg.append("svg:g")
              .attr("class", "y axis")
              .attr("transform", "translate(400,0)")
              .call(yaxis);
        
    redraw()
    controller2.typer.setfocus()
    });


function changemode(newmode) {

    // save our mode as a global
    mode = newmode;

    // turn off any previously selected modebox modes, turn on new mode
    d3.selectAll(".selected").classed("selected", false);
    d3.select("#"+mode).classed("selected", true);
    
    // turn off any visible sidebars, turn on current sidebar
    d3.selectAll(".righthand").style("display","none");
    d3.select("#"+mode+"sidebar").style("display","block");
    

    switch (mode){
        case "view":
            enter_view_mode();
            break;
        case "geom":
            enter_geom_mode();
            break;
        case "stress":
            enter_stress_mode();
            break;
    }
}

function redraw(){

    console.log("Redrawing...");
    

    // Bind edge data to visualization via mID
    // Gives us object constancy -> nice animated transitions
    edges = svg.selectAll(".edge")
        .data(state.vis.edges, function(d){return d['mid']});

    // Enter function for edges.
    // Formats each incoming edge
    edges.enter()
        .insert("line")
        .attr("class", "edge")
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
            controller2.typer.setfocus()
            })

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
        .classed("unselected","true")
        .classed("node","true")
        .attr("r", 5)
        .attr("cx", function(d, i) {
            return xscale(d["x"]);
            })
        .attr("cy", function(d, i) {
            return yscale(d["y"]);
            })
        .on("click", function(d) { 
            controller2.typer.consoleInsert(" n"+d['iid']);
            controller2.typer.setfocus() 
            //d['iid']);
            })
        .on("mouseout", function(d) {d3.select(this).attr("class", "node unselected");})
        .on("mouseover", function() {d3.select(this).attr("class","node selected");});
    nodes.transition().duration(500)
            .attr("cx", function(d, i) {
            return xscale(d["x"]);
            })
        .attr("cy", function(d, i) {
            return yscale(d["y"]);
            });

    nodes.exit().remove();
    
    node_entries = d3.select("#nodeslist").selectAll(".toplevel")
        .data(state.vis.nodes)
        .enter()
        .insert("li")
        .attr("class","toplevel")

    node_entries
        .html(function (d){
            var part1 =  "<div class='collapsed'>";
            var part2 = "Node "+d.iid+" @("+d.x + ", " + d.y+")</div>";
            var part3 = "<ul><li>Color: "+d.color + "</li><li>Food: delicious</li></ul>"
            return part1+part2+part3; 
        });
  
    
    edge_entries = d3.select("#edgeslist").selectAll(".toplevel")
        .data(state.vis.edges)
        .enter()
        .insert("li")
        .attr("class", "toplevel");
    
    edge_entries.html(function(d) {
            var part1 =  "<div class='collapsed'>";
            var part2 = "Edge "+d.mid+": "+state.vis.nodes[d.i0].iid + " -> " + state.vis.nodes[d.i1].iid+")</div>";
            var part3 = "<ul><li>Color: "+d.color + "</li><li>Food: delicious</li></ul>"
            return part1+part2+part3; 
        });

    function collapse(d,i){
        d3.select(this).classed("collapsed", true)
                       .classed("expanded", false)
                       .on("click", expand);
        }
    
    function expand(d,i){
        d3.selectAll(".toplevel").select("div")
                .classed("expanded",false)
                .classed("collapsed", true);

        d3.select(this).classed("collapsed", false)
                       .classed("expanded", true)
                       .on("click", collapse);
        }

    d3.selectAll(".collapsed").on("click", expand);
    d3.selectAll(".expanded").on("click", collapse);
    changemode(mode);

};

