
// Every time we switch modes, we change out the various mouse
// callbacks and repaint some of the geometry.
//
//  * Click bg to add node
//  * Click nodes to add edge
//  * Ctrl-click to delete a node/edge
//  * Drag to manually move a node


function enter_geom_mode(){

    selectedNode=-1;
    console.log("Switched to geom mode");

    var drag = d3.behavior.drag()
        .origin(Object)
        .on("drag", on_node_drag);

    d3.selectAll(".node")
        .attr("fill", "black")
        .on("mouseout", on_node_mouseout) 
        .on("mouseover", on_node_mouseover)
        .on("click", on_node_click)
        .call(drag);

    d3.selectAll(".edge")
        .attr("fill","gray");

    d3.select("svg")
        .on("click", on_bg_click);

}


function on_node_mouseout(d,i){
    if (d["iid"] == selectedNode) {
        d3.select(this).attr("fill","fuchsia");
    }
    else {
        d3.select(this).attr("fill","black");
    }
};

function on_node_mouseover(d,i){
    if (d["iid"]==selectedNode) {
        d3.select(this).attr("fill","fuchsia");
    }
    else {
        d3.select(this).attr("fill","red");
    }
};

function on_node_click(d,i) {
    if (selectedNode == -1) {
        selectedNode = d["iid"];
    }
    else {
        if (selectedNode != d['iid']) {
            send("edge n"+selectedNode+" n"+d['iid']);
        }
        nodes.attr("fill","black");
        selectedNode = d["iid"];
    }
    d3.select(this).attr("fill","fuchsia");
    d3.event.stopPropagation();
    controller2.typer.setfocus()
};

function on_bg_click(d) {
    var mouse = d3.mouse(this);
    var x = Math.round(xscale.invert(mouse[0])*1000)/1000;
    var y = Math.round(yscale.invert(mouse[1])*1000)/1000;

    send("node "+x+" "+y);
    //controller2.typer.consoleInsert("node "+x+" "+y);
    controller2.typer.setfocus();
}


function on_node_drag(d,i) {
    console.log("Dragging "+d3.event.x + ", " + d3.event.y);
    console.log("Data was "+ d.x + ", " + d.y);
    d3.select(this)
        .attr("cx", d3.event.x) 
        .attr("cy", d3.event.y);

    d.x = xscale.invert(d3.event.x);
    d.y = yscale.invert(d3.event.y);
    console.log("Dragging "+d3.event.x + ", " + d3.event.y);
    console.log("Data now "+ d.x + ", " + d.y);
    console.log("JSON now "+state['geom']['nodes'][i]['x']);
}




