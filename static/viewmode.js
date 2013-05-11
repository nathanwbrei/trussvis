
// Contains all of the callbacks to handle View Mode, wherein the user may:
//   * Load a file
//   * Save a file
//   * Zoom on scroll
//   * Pan on mousedrag
//   * Zooms to window on rightmousedrag
//   * Move axes?
//   * Set grid?
//   * Snap to grid?


function enter_view_mode() {
    edges = d3.selectAll('.edge')
        .transition()
        .duration(500)
        .attr("stroke", "white");
    console.log("Entered view mode, repainted edges.");
}

