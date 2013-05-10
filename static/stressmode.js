
function enter_stress_mode() {
    if (state['msg'] != "Calculated statics.") {
        send("stress");
    }
    d3.selectAll('edge').transition().duration(500)
        .attr("stroke", function(d,i) {
            return d["color"];
        });
}



