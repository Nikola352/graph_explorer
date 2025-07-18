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

    d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).distance(300))
            .force("charge", d3.forceManyBody().strength(100))
            .force("center", d3.forceCenter(1000 / 2, 700 / 2))
            .force("gravity", d3.forceManyBody().strength(-100))
            .force("collide", d3.forceCollide().radius(80))
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
});
