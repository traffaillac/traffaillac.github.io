function scatterplot(id, data, ints, i, j) {
	let margin = {top: 6, right: 30, bottom: 18, left: 60};
	let width = id.clientWidth;
	let height = id.clientHeight;
	let x = d3.scaleLinear()
		.domain(ints[i]).nice()
		.range([margin.left, width - margin.right]);
	let y = d3.scaleLinear()
		.domain(ints[j]).nice()
		.range([height - margin.bottom, margin.top]);
	id.xscale = x;
	id.yscale = y;
	let svg = d3.select(id)
		.style("user-select", "none")
	svg.selectAll('*').remove();
	svg.append("g")
		.attr("transform", `translate(0,${height - margin.bottom})`)
		.call(d3.axisBottom(x))
		/*.append("text")
		.attr("x", width - margin.right)
		.attr("y", 32)
		.attr("fill", "#000")
		.attr("text-anchor", "end")
		.attr("font-size", 16)
		.text(cols[i].substr(10));*/
	svg.append("g")
		.attr("transform", `translate(${margin.left},0)`)
		.call(d3.axisLeft(y))
		/*.append("text")
		.attr("x", 0)
		.attr("y", margin.top - 10)
		.attr("fill", "#000")
		.attr("text-anchor", "middle")
		.attr("font-size", 16)
		.text(cols[j].substr(10));*/
	let points = svg.append("g")
		.selectAll("circle")
		.data(data)
		.join("circle")
		.attr("cx", d => x(d[i]))
		.attr("cy", d => y(d[j]))
		.attr("r", d => 1 + 2 * Math.sqrt(d[d.length-1]))
		.on("mouseenter", e => {
			let bounds = e.target.getBoundingClientRect();
			tooltip.style.left = bounds.left + "px";
			tooltip.style.top = (bounds.top + bounds.bottom) / 2 + "px";
			tooltip.innerHTML = cols.map((c, i) => `${c} : <b>${e.target.__data__[i].toFixed(2)}</b>`).join("<br>") + `<br>Echantillons : <b>${e.target.__data__[cols.length]}</b>`
			tooltip.style.display = null; })
		.on("mouseout", e => {
			tooltip.style.display = "none"; })
	svg.append("rect")
		.attr("display", "none")
		.attr("fill", "none")
		.attr("stroke", "#000")
		.attr("stroke-dasharray", "5,5")
		.style("pointer-events", "none")
}
