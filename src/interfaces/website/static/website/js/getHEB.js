const buildHEB = (hebId, hebData) => {
    const diameter = 600,
        radius = diameter / 2,
        innerRadius = radius - 120;

    const cluster = d3.cluster()
        .size([360, innerRadius]);

    const line = d3.radialLine()
        .curve(d3.curveBundle.beta(0.85))
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    const radiusTransform = radius + 50;

    const svg = d3.select(hebId)
        .append("center")
        .append("svg")
        .attr("font-family", "sans-serif")
        .attr("font-size", 6)
        .attr("width", diameter+200)
        .attr("height", diameter+200)
        .append("g")
        .attr("transform", "translate(" + radiusTransform + "," + radiusTransform + ")");

    let link = svg.append("g").selectAll(".link"),
        node = svg.append("g").selectAll(".node");

    const root = packageHierarchy(hebData)
        .sum(function(d) { return d.size; });

    cluster(root);

    link = link
        .data(packageImports(root.leaves()))
        .enter().append("path")
        .each(function(d)
        {
            d.source = d[0];
            d.target = d[d.length - 1];
        })
        .attr("class", "link")
        .attr("d", line);

    node = node
        .data(root.leaves())
        .enter().append("text")
        .attr("class", "node")
        .attr("dy", "0.31em")
        .attr("transform", function(d)
        { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
        .attr("text-anchor", function(d)
        { return d.x < 180 ? "start" : "end"; })
        .text(function(d)
        { return d.data.name; })
        .on("mouseover", mouseOvered)
        .on("mouseout", mouseOuted);

    function mouseOvered(d) {
        node
            .each(function(n) { n.target = n.source = false; });

        link
            .classed("link--target", function(l) { if (l.target === d) return l.source.source = true; })
            .classed("link--source", function(l) { if (l.source === d) return l.target.target = true; })
            .filter(function(l) { return l.target === d || l.source === d; })
            .raise();

        node
            .classed("node--target", function(n) { return n.target; })
            .classed("node--source", function(n) { return n.source; });
    }

    function mouseOuted(d) {
        link
            .classed("link--target", false)
            .classed("link--source", false);

        node
            .classed("node--target", false)
            .classed("node--source", false);
    }

    function packageHierarchy(classes) {
        let map = {};

        function find(name, data) {
            let node = map[name], i;
            if (!node) {
                node = map[name] = data || {name: name, children: []};
                if (name.length) {
                    node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
                    node.parent.children.push(node);
                    node.key = name.substring(i + 1);
                }
            }
            return node;
        }

        classes.forEach(function(d) {
            find(d.name, d);
        });

        return d3.hierarchy(map[""]);
    }

    function packageImports(nodes) {
        let map = {},
            imports = [];

        nodes.forEach(function(d) {
            map[d.data.name] = d;
        });

        nodes.forEach(function(d) {
            if (d.data.imports) d.data.imports.forEach(function(i) {
                imports.push(map[d.data.name].path(map[i]));
            });
        });

        return imports;
    }

    return svg;
}

const getHEBData = (hebDataId) => {
    const $data = $(hebDataId);
    return JSON.parse($data[0].textContent);
}

const reduceHebEdges = (items) => {
    return items.reduce(
        (previous, next) => {
            let organism = next.organism;
            let regulator = next.regulator;
            let gene = next.gene;
            let interaction = next.protrend_id;
            let effector = next.effector;
            let tfbs = next.tfbs;

            let regulatorName = organism + '.reg.' + regulator;
            let geneName = organism + '.gen.' + gene;
            let interactionName = organism + '.int.' + interaction;

            previous[regulatorName] = previous[regulatorName] || new Set();
            previous[geneName] = previous[geneName] || new Set();
            previous[interactionName] = previous[interactionName] || new Set();

            previous[geneName].add(regulatorName);
            previous[interactionName].add(geneName);
            previous[interactionName].add(regulatorName);

            if (effector && tfbs) {
                let effectorName = organism + '.efc.' + effector;
                let tfbsName = organism + '.bs.' + tfbs;

                previous[effectorName] = previous[effectorName] || new Set();
                previous[tfbsName] = previous[tfbsName] || new Set();

                previous[regulatorName].add(effectorName);
                previous[geneName].add(regulatorName);
                previous[tfbsName].add(regulatorName);
                previous[tfbsName].add(geneName);
                previous[interactionName].add(effectorName);
                previous[interactionName].add(regulatorName);
                previous[interactionName].add(geneName);
                previous[interactionName].add(tfbsName);

                return {...previous,
                    [regulatorName]: previous[regulatorName],
                    [geneName]: previous[geneName],
                    [interactionName]: previous[interactionName],
                    [effectorName]: previous[effectorName],
                    [tfbsName]: previous[tfbsName]};

            } else if (effector) {
                let effectorName = organism + '.efc.' + effector;

                previous[effectorName] = previous[effectorName] || new Set();
                previous[regulatorName].add(effectorName);
                previous[geneName].add(regulatorName);
                previous[interactionName].add(effectorName);
                previous[interactionName].add(regulatorName);
                previous[interactionName].add(geneName);

                return {...previous,
                    [regulatorName]: previous[regulatorName],
                    [geneName]: previous[geneName],
                    [interactionName]: previous[interactionName],
                    [effectorName]: previous[effectorName]};

            } else if (next.tfbs) {
                let tfbsName = organism + '.bs.' + next.tfbs;

                previous[tfbsName] = previous[tfbsName] || new Set();
                previous[tfbsName].add(regulatorName);
                previous[tfbsName].add(geneName);
                previous[geneName].add(regulatorName);
                previous[interactionName].add(regulatorName);
                previous[interactionName].add(geneName);
                previous[interactionName].add(tfbsName);
                return {...previous,
                    [regulatorName]: previous[regulatorName],
                    [geneName]: previous[geneName],
                    [interactionName]: previous[interactionName],
                    [tfbsName]: previous[tfbsName]};
            }
            else {
                return {...previous,
                    [regulatorName]: previous[regulatorName],
                    [geneName]: previous[geneName],
                    [interactionName]: previous[interactionName]};
            }
        }, {});
}

const filterHebData = (regulatorsIds, data) => {
    const filteredInteractions = data.regulatory_interaction.filter(
        function (item) {
            return regulatorsIds.some(
                function (id) {
                    return item.regulator === id;
                });
        });
    const interactions = filteredInteractions.map(
        function (item) {
            const organism = "org";
            return {
                "organism": organism,
                "regulator": item.regulator,
                "gene": item.gene,
                "protrend_id": item.protrend_id,
                "effector": item.effector,
                "tfbs": item.tfbs
            };
        });
    const edges = reduceHebEdges(interactions);
    let hebEntries = [];
    for (const [key, value] of Object.entries(edges)) {
        hebEntries.push(
            {
                "name": key,
                "imports": Array.from(value)
            }
        );
    }
    return hebEntries;
};

const getHEB = (hebBtnId, hebTableId,
                closeHEBModal1Id, closeHEBModal2Id,
                hebId, hebDataId) => {
    let heb = null;
    const $btn = $(hebBtnId);
    const $table = $(hebTableId);
    const data = getHEBData(hebDataId);

    function getSelections() {
        return $.map($table.bootstrapTable('getSelections'),
            function (row) {
                return row.id
            })
    }

    $table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table',
        function () {
            const nSelected = $table.bootstrapTable('getSelections').length;
            if (nSelected > 0 && nSelected < 16) {
                $btn.prop('disabled', false);
            }
            else {
                $btn.prop('disabled', true);
            }
        }
    );

    $btn.click(
        function () {
            const regulatorsIds = getSelections();
            const filteredData = filterHebData(regulatorsIds, data);
            heb = buildHEB(hebId, filteredData);
            $btn.prop('disabled', true)
            $table.bootstrapTable('uncheckAll');
        }
    );

    const closeHEBModalHandler = function (event) {
        const hebElement = document.querySelector(hebId);
        hebElement.replaceChildren();
    };

    document.querySelector(closeHEBModal1Id).addEventListener('click', closeHEBModalHandler);
    document.querySelector(closeHEBModal2Id).addEventListener('click', closeHEBModalHandler);
    return heb;
}