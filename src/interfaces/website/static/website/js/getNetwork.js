const getNetworkStyle = () => {
    return [
        {
            "selector": "core",
            "style": {
                "selection-box-color": "#AAD8FF",
                "selection-box-border-color": "#8BB0D0",
                "selection-box-opacity": "0.5"
            }
        }, {
            "selector": "node",
            "style": {
                "width": "mapData(score, 0, 0.006769776522008331, 20, 60)",
                "height": "mapData(score, 0, 0.006769776522008331, 20, 60)",
                "content": "data(name)",
                "font-size": "12px",
                "text-valign": "center",
                "text-halign": "center",
                "background-color": "#555",
                "text-outline-color": "#555",
                "text-outline-width": "2px",
                "color": "#fff",
                "overlay-padding": "6px",
                "z-index": "10"
            }
        }, {
            "selector": "node[?attr]",
            "style": {
                "shape": "rectangle",
                "background-color": "#aaa",
                "text-outline-color": "#aaa",
                "width": "16px",
                "height": "16px",
                "font-size": "6px",
                "z-index": "1"
            }
        }, {
            "selector": "node[?query]",
            "style": {
                "background-clip": "none",
                "background-fit": "contain"
            }
        }, {
            "selector": "node:selected",
            "style": {
                "border-width": "6px",
                "border-color": "#AAD8FF",
                "border-opacity": "0.5",
                "background-color": "#77828C",
                "text-outline-color": "#77828C"
            }
        }, {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "opacity": "0.4",
                "line-color": "#bbb",
                "width": "mapData(weight, 0, 1, 1, 8)",
                "overlay-padding": "3px"
            }
        }, {
            "selector": "node.unhighlighted",
            "style": {
                "opacity": "0.2"
            }
        }, {
            "selector": "edge.unhighlighted",
            "style": {
                "opacity": "0.05"
            }
        }, {
            "selector": ".highlighted",
            "style": {
                "z-index": "999999"
            }
        }, {
            "selector": "node.highlighted",
            "style": {
                "border-width": "6px",
                "border-color": "#AAD8FF",
                "border-opacity": "0.5",
                "background-color": "#394855",
                "text-outline-color": "#394855"
            }
        }, {
            "selector": "edge.filtered",
            "style": {
                "opacity": "0"
            }
        }, {
            "selector": "edge[group=\"1\"]",
            "style": {
                "line-color": "#151515"
            }
        }, {
            "selector": "edge[group=\"2\"]",
            "style": {
                "line-color": "#A63D40"
            }
        }, {
            "selector": "edge[group=\"3\"]",
            "style": {
                "line-color": "#E9B872"
            }
        }, {
            "selector": "edge[group=\"4\"]",
            "style": {
                "line-color": "#90A959"
            }
        }, {
            "selector": "edge[group=\"5\"]",
            "style": {
                "line-color": "#6494AA"
            }
        }, {
            "selector": "edge[group=\"6\"]",
            "style": {
                "line-color": "#fc6000"
            }
        }, {
            "selector": "edge[group=\"7\"]",
            "style": {
                "line-color": "#96ea00"
            }
        }, {
            "selector": "edge[group=\"8\"]",
            "style": {
                "line-color": "#339a74"
            }
        }, {
            "selector": "edge[group=\"9\"]",
            "style": {
                "line-color": "#123127"
            }
        }, {
            "selector": "edge[group=\"10\"]",
            "style": {
                "line-color": "#5E4C5A"
            }
        }, {
            "selector": "edge[group=\"11\"]",
            "style": {
                "line-color": "#63ec53"
            }
        }, {
            "selector": "edge[group=\"12\"]",
            "style": {
                "line-color": "#5DA9E9"
            }
        }, {
            "selector": "edge[group=\"13\"]",
            "style": {
                "line-color": "#003F91"
            }
        }, {
            "selector": "edge[group=\"14\"]",
            "style": {
                "line-color": "#f53030"
            }
        }, {
            "selector": "edge[group=\"15\"]",
            "style": {
                "line-color": "#6D326D"
            }
        }
    ];
}

const buildNetwork = (networkId, networkConfig, networkData) => {

    const h = function (tag, attrs, children) {
        const el = document.createElement(tag);

        Object.keys(attrs).forEach(function (key) {
            const val = attrs[key];

            el.setAttribute(key, val);
        });

        children.forEach(function (child) {
            el.appendChild(child);
        });

        return el;
    };

    const t = function (text) {
        return document.createTextNode(text);
    };

    const $ = document.querySelector.bind(document);

    const cy = window.cy = cytoscape({
        container: document.querySelector(networkId),
        style: getNetworkStyle(),
        elements: networkData,
        layout: {name: 'random'}
    });

    const params = {
        name: 'cola',
        nodeSpacing: 5,
        edgeLengthVal: 45,
        animate: true,
        randomize: false,
        maxSimulationTime: 1500
    };

    let layout = makeLayout();

    layout.run();

    const $btnParam = h('div', {
        'class': 'param'
    }, []);

    const $Preamble = h('div', {
        'class': 'preamble'
    }, []);

    $Preamble.appendChild(h('div', {
        'class': 'label label-info fs-4 pb-2'
    }, [t("Network Visualization")]));
    $Preamble.appendChild(h('p', {}, [t("Please click on the randomizer and down arrow to fit the network to the screen.")]));
    $Preamble.appendChild(h('p', {}, [t("Adjust edge length or node spacing if desired.")]));
    $Preamble.appendChild(h('p', {}, [t("You can zoom in/out using the scroll wheel on your mouse.")]));
    $Preamble.appendChild(h('p', {}, [t("Nodes and edges can be clicked to show more info.")]));

    const $config = $(networkConfig);

    $config.appendChild( $Preamble );
    $config.appendChild( $btnParam );

    const sliders = [
        {
            label: 'Edge length',
            param: 'edgeLengthVal',
            min: 1,
            max: 5
        },

        {
            label: 'Node spacing',
            param: 'nodeSpacing',
            min: 1,
            max: 5
        }
    ];

    const buttons = [
        {
            label: h('span', { 'class': 'fa fa-random' }, []),
            layoutOpts: {
                randomize: true,
                flow: null
            }
        },

        {
            label: h('span', { 'class': 'fa fa-long-arrow-down' }, []),
            layoutOpts: {
                flow: { axis: 'y', minSeparation: 30 }
            }
        }
    ];

    sliders.forEach( makeSlider );

    buttons.forEach( makeButton );

    function makeLayout( opts ){
        params.randomize = false;
        params.edgeLength = function(e){ return params.edgeLengthVal / e.data('weight'); };

        for( const i in opts ){
            params[i] = opts[i];
        }

        return cy.layout( params );
    }

    function makeSlider( opts ){
        const $input = h('input', {
            id: 'slider-'+opts.param,
            type: 'range',
            min: opts.min,
            max: opts.max,
            step: 1,
            value: params[ opts.param ],
            'class': 'slider'
        }, []);

        const $param = h('div', { 'class': 'param' }, []);

        const $label = h('label', { 'class': 'label label-default', for: 'slider-'+opts.param }, [ t(opts.label) ]);

        $param.appendChild( $label );
        $param.appendChild( $input );

        $config.appendChild( $param );

        const update = _.throttle(function(){
            params[ opts.param ] = $input.value;

            layout.stop();
            layout = makeLayout();
            layout.run();
        }, 1000/30);

        $input.addEventListener('input', update);
        $input.addEventListener('change', update);
    }

    function makeButton( opts ){
        const $button = h('button', { 'class': 'btn btn-default' }, [ opts.label ]);

        $btnParam.appendChild( $button );

        $button.addEventListener('click', function(){
            layout.stop();

            if( opts.fn ){ opts.fn(); }

            layout = makeLayout( opts.layoutOpts );
            layout.run();
        });
    }

    const makeTippy = function(node, html){
        return tippy( node.popperRef(), {
            html: html,
            trigger: 'manual',
            arrow: true,
            placement: 'bottom',
            hideOnClick: false,
            interactive: true
        } ).tooltips[0];
    };

    const hideTippy = function (node) {
        const tippy = node.data('tippy');

        if (tippy != null) {
            tippy.hide();
        }
    };

    const hideAllTippies = function () {
        cy.nodes().forEach(hideTippy);
        cy.edges().forEach(hideTippy);
    };

    cy.on('tap', function(e){
        if(e.target === cy){
            hideAllTippies();
        }
    });

    cy.on('zoom pan', function(e){
        hideAllTippies();
    });

    cy.nodes().forEach(function(n){
        const uniprot_accession = n.data('uniprot_accession');
        const uniprot_links = [h('p', {'class': 'network-node-paragraph'}, [ t('UNIPROT: ' + uniprot_accession) ])];

        const protrend_ids = n.data('protrend_ids');
        const protrend_links = protrend_ids.map(function (protrend_id) {
            return h('p', {'class': 'network-node-paragraph'}, [ t('PROTREND: ' + protrend_id) ]);
        });

        const links = protrend_links.concat(uniprot_links)
        const tippy = makeTippy(n, h('div', {}, links));

        n.data('tippy', tippy);

        n.on('click', function(e){
            tippy.show();

            cy.nodes().not(n).forEach(hideTippy);
        });
    });

    cy.edges().forEach(function(n){
        const interactions = n.data('interaction');
        const effects = n.data('effect');

        let zip = (a1, a2) => a1.map((x, i) => [x, a2[i]]);

        const links = zip(interactions, effects).map(function (interaction) {
            return h('a', {
                target: '_blank',
                href: interaction[0],
                'class': 'network-edge-paragraph'
            }, [t(interaction[0] + ' - ' + interaction[1])]);
        });

        const tippy = makeTippy(n, h('div', {}, links));

        n.data('tippy', tippy);

        n.on('click', function(e){
            tippy.show();

            cy.edges().not(n).forEach(hideTippy);
        });
    });

    return cy;
}

const getNetworkData = (networkDataId) => {
    const $data = $(networkDataId);
    return JSON.parse($data[0].textContent);
}

const reduceNetworkNodes = (items) => {
    return items.reduce(
        (previous, next) => {
            previous[next.locus_tag] = previous[next.locus_tag] ||
                {"data":
                        {"id": next.locus_tag,
                            "protrend_ids": [],
                            "name": next.locus_tag,
                            "uniprot_accession": next.uniprot_accession,
                            "score": 0.5,
                            "query": true},
                    "group": "nodes",
                    "removed": false,
                    "selected": false,
                    "selectable": true,
                    "locked": false,
                    "grabbed": false,
                    "grabbable": true};

            previous[next.locus_tag].data.protrend_ids.push(next.protrend_id);

            return {...previous, [next.locus_tag]: previous[next.locus_tag]};
        }, {});
}

const reduceNetworkEdges = (items, filteredRegulators, filteredGenes) => {
    return items.reduce(
        (previous, next) => {
            let regulator = filteredRegulators.find(
                function (item) {
                    return item.protrend_id === next.regulator;
                });
            let gene = filteredGenes.find(
                function (item) {
                    return item.protrend_id === next.gene;
                });

            let source = regulator.locus_tag;
            let target = gene.locus_tag;
            let group = filteredRegulators.findIndex(
                function (item) {
                    return item.protrend_id === next.regulator;
                });
            let edgeId = source + "-" + target;

            previous[edgeId] = previous[edgeId] ||
                {"data":
                        {"source": source,
                            "target": target,
                            "weight": 0.5,
                            "interaction": [],
                            "effect": [],
                            "group": "" + group,
                            "id": edgeId},
                    "position": {},
                    "group": "edges",
                    "removed": false,
                    "selected": false,
                    "selectable": true,
                    "locked": false,
                    "grabbed": false,
                    "grabbable": true
                };

            previous[edgeId].data.interaction.push(next.protrend_id);
            previous[edgeId].data.effect.push(next.regulatory_effect);
            return {...previous, [edgeId]: previous[edgeId]};
        }, {});
}

const filterNetworkData = (regulatorsIds, data) => {
    const filteredRegulators = data.regulator.filter(
        function (item) {
            return regulatorsIds.some(
                function (id) {
                    return item.protrend_id === id;
                });
        });

    const filteredInteractions = data.regulatory_interaction.filter(
        function (item) {
            return filteredRegulators.some(
                function (regulator) {
                    return item.regulator === regulator.protrend_id;
                });
        });

    filteredGenes = data.gene.filter(
        function (item) {
            return filteredInteractions.some(
                function (interaction) {
                    return item.protrend_id === interaction.gene;
                });
        });

    const nodes = reduceNetworkNodes(filteredRegulators.concat(filteredGenes));
    const edges = reduceNetworkEdges(filteredInteractions, filteredRegulators, filteredGenes);

    const nodesValues = Object.keys(nodes).map(function(key) {
        return nodes[key];
    });
    const edgesValues = Object.keys(edges).map(function(key) {
        return edges[key];
    });
    return nodesValues.concat(edgesValues);
}

const hideTippy = function (node) {
    const tippy = node.data('tippy');

    if (tippy != null) {
        tippy.hide();
    }
};

const hideAllTippies = function (network) {
    network.nodes().forEach(hideTippy);
    network.edges().forEach(hideTippy);
};

const getNetwork = (networkBtnId, networkTableId,
                    closeNetworkModal1Id, closeNetworkModal2Id,
                    networkId, networkConfigId,
                    networkDataId) => {
    let network = null;
    const $btn = $(networkBtnId);
    const $table = $(networkTableId);
    const data = getNetworkData(networkDataId);

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
            const filteredData = filterNetworkData(regulatorsIds, data);
            network = buildNetwork(networkId, networkConfigId, filteredData);
            $btn.prop('disabled', true)
            $table.bootstrapTable('uncheckAll');
        }
    );

    const closeNetworkModalHandler = function (event) {
        const networkElement = document.querySelector(networkId);
        networkElement.replaceChildren();

        const networkConfigElement = document.querySelector(networkConfigId);
        networkConfigElement.replaceChildren();

        hideAllTippies(network);
    };

    document.querySelector(closeNetworkModal1Id).addEventListener('click', closeNetworkModalHandler);
    document.querySelector(closeNetworkModal2Id).addEventListener('click', closeNetworkModalHandler);

    return network;
}