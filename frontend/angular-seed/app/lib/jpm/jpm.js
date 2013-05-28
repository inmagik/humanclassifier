(function(){
	
	var jpm = window.jpm = {};


	/*jpm.tree = function(data){

		var tree = { children:[] },
	        classes = ,
	        path = [],
	        leaf = {};

	    try {
	        
	        data.forEach(function(d){

	          	// Structure path
	            path = model.structure.hierarchy.value.map(function(p){ return d[p.key]; })
	            leaf = raw.seek(tree, path, classes);
	            if(leaf === false) return;
	            if (!leaf.map) leaf.map = {};


	            // Mapping options...
	            for (var m in model.map){
	            	if (!leaf.map.hasOwnProperty(m)) leaf.map[m] = 0;
	            	leaf.map[m] = model.map[m].map(d, leaf.map[m]) || null;
	            }

	            delete leaf.children;

		    });
        }
        catch(e){
        	console.log(e.message)
          	return false;
        }
    
    	return tree;
		},
	}*/

	jpm.bubbles = function(){

		var vis = {},
			data,
			svg,
			target,
			groupBy;

		vis.update = function(){

			if (!data || !target) return;


			var diameter = 300,
			    format = d3.format(",d"),
			    color = d3.scale.category20c();

			var bubble = d3.layout.pack()
			    .sort(null)
			    .size([diameter, diameter])
			    .value(function(d){return Math.random();})
			    .padding(1.5);

			svg = target.append("svg:svg")
			    .attr("width", diameter)
			    .attr("height", diameter)
			    .attr("class", "bubble");


			  var node = svg.selectAll(".node")
			      .data(bubble.nodes(classes({"name":"ciao", "children":data}))
			      .filter(function(d) { return !d.children; }))
			    .enter().append("g")
			      .attr("class", "node")
			      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

			  node.append("title")
			      .text(function(d) { return d.className + ": " + format(d.value); });

			  node.append("circle")
			      .attr("r", function(d) { return d.r; })
			      .style("fill", function(d) { return color(d.packageName); });

			  node.append("text")
			      .attr("dy", ".3em")
			      .style("text-anchor", "middle")
			      .text(function(d) { return d.className.substring(0, d.r / 3); });

			// Returns a flattened hierarchy containing all leaf nodes under the root.
			function classes(root) {
			  var classes = [];

			  function recurse(name, node) {
			    if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
			    else classes.push({packageName: name, className: node.name, value: node.size});
			  }

			  recurse(null, root);
			  return {children: classes};
			}


		    return this;



		}

		vis.data = function(x){
			if (!arguments.length) return data;
				data = x;
				return vis;
		}

		vis.target = function(x){
			if (!arguments.length) return target;
			console.log(d3.select(x));
			target = d3.select(x[0]);
			return vis;
		}

		return vis;

	}

})();