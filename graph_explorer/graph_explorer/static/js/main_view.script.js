document.addEventListener("DOMContentLoaded", () => {
    const svg = d3.select("svg[id^='svg-']");
  
    const nodeElements = svg.selectAll("g.node[enabled='true']").nodes();
    const linkElements = svg.selectAll("path.link[enabled='true']").nodes();

    const nodes = nodeElements.map(elem => {
        const data = elem.__data__
        return {
            id: elem.id, 
            ...data,
        };
    });

    const links = linkElements.map(elem => {
    const data = elem.__data__;
    return {
            ...data,
            source: nodes.find(n => n.id === elem.__data__.source.id),
            target: nodes.find(n => n.id === elem.__data__.target.id)
        };
    });

    const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).distance(350))
            .force("charge", d3.forceManyBody().strength(100))
            .force("center", d3.forceCenter(500, 400))
            .force("gravity", d3.forceManyBody().strength(-100))
            .force("collide", d3.forceCollide().radius(100))
        .on("tick",tick)

    function tick() {
        svg.selectAll("path.link")
        .data(links)
        .attr("d", function(d) {
            const reverse = links.find(l => l.source.id === d.target.id && l.target.id === d.source.id);

            if (reverse && reverse !== d) {
                const offset = 20;

                const dx = d.target.x - d.source.x;
                const dy = d.target.y - d.source.y;
                const dist = Math.sqrt(dx*dx + dy*dy);

                const nx = -dy / dist;
                const ny = dx / dist;

                const mx = (d.source.x + d.target.x)/2 + nx * offset;
                const my = (d.source.y + d.target.y)/2 + ny * offset;

                return `M${d.source.x},${d.source.y} L${mx},${my} L${d.target.x},${d.target.y}`;
            } else {
                return `M${d.source.x},${d.source.y} L${d.target.x},${d.target.y}`;
            }
        });
        svg.selectAll("g.node")
        .data(nodes).attr("transform", d => `translate(${d.x},${d.y})`);
    }

    d3.selectAll("g.node[drag='true']")
        .call(d3.drag()
        .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        })
        .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
        })
        .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
        }));

    var g = d3.select("svg[zoom='true'] g");
    const handleZoom = (e) => g.attr('transform', e.transform);
    const zoom = d3.zoom().on('zoom', handleZoom);
    d3.selectAll("svg[zoom='true']").call(zoom);

    d3.selectAll("g.node[click-focus='true']")
        .on("click", function(event, d) {
            handleNodeFocus(d.id);
    });

    function handleNodeFocus(nodeId){
        d3.selectAll(".active-node").select("circle")
            .style("fill", "white")
            .style("stroke", "#04446fff")
            .style("stroke-width", "1.5px");
        d3.selectAll(".active-node").classed("active-node", false);

        const focusedNode = g.selectAll(".node")
            .filter(d => d.id === nodeId);
        focusedNode.classed("active-node", true);
        focusedNode.select("circle")
            .style("fill", "white")  
            .style("stroke", "#04446fff") 
            .style("stroke-width", "4px");
        focusedNode.select("text").style("fill", "#04446fff");

        if (!focusedNode.empty()) {
            const svg = d3.select("svg[zoom='true']");
            const svgNode = svg.node();
            console.log(svg)
            console.log(svgNode)
            const transform = d3.zoomTransform(svgNode);

            const svgWidth = svgNode.clientWidth;
            const svgHeight = svgNode.clientHeight;

            const nodeDatum = focusedNode.datum();
            const targetX = nodeDatum.x;
            const targetY = nodeDatum.y;

            const newTransform = d3.zoomIdentity
                .translate(svgWidth / 2 - targetX * transform.k, svgHeight / 2 - targetY * transform.k)
                .scale(transform.k);

            svg.transition()
                .duration(750)
                .call(zoom.transform, newTransform);
        }
    }
});
