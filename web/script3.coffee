graph = (e, data) ->

	contain = d3.select(".content")
	# svg = contain.append("svg").attr(height: "100%").attr(width: "100%")

	dataByHousehold = d3.nest()
		.key((d) -> d.respondent)
		.entries(data)

	dataByDate = d3.nest()
		.key((d) -> d["OUTPUT_DATE"])
		.entries(data)

	console.log dataByDate

	dayIndex = 119

	dayData = dataByDate[dayIndex].values.filter((d) -> d["TYPE"] is "general")

	dayData = ({id: day["respondent"], data: day["OUTPUT_DATE"], entries: d3.entries(day).slice(3)} for day in dayData)

	dayMin = d3.min(dayData, (d) -> d3.min(d.entries, (e) -> +e.value))
	dayMax = d3.max(dayData, (d) -> d3.max(d.entries, (e) -> +e.value))

	numHouseholds = dataByHousehold.length
	dataLength = dayData[0].entries.length
	console.log dataLength

	size = 100
	baseSpeed = 1000 #1000 = 30min per sec
	multiplier = 1
	speed = baseSpeed * multiplier
	index = 0
	elapsed = 0
	width = 1000
	height = 800
	startSunrise = 0
	startSunset = 12 * 2
	dateFormat = d3.time.format("%I:%M%p")
	# console.log indexOfSunrise, indexOfSunset

	dayScale = d3.scale.pow().domain([dayMin, dayMax]).range([0, size/2])
	timeScale = d3.time.scale().range([1, 100])
	# posScale = d3.scale.linear().domain([dayMin, dayMax]).range([height - 200, 200])

	body = d3.select("body")
	svg = contain.append("svg")
		.attr(width: width)
		.attr(height: height)

	timeText = contain.append("div").attr(class: "time")
	timeLine = contain.append("div").attr(class: "timeline").append("svg").attr(width: "100%").attr(height: 40)


	body.style(background: "#000")

	body.transition()
		.duration(speed * startSunset)
		.style(background: "#454f5a")
	bg = "light"

	circles = svg.selectAll("circle")
		.data(dayData)
		.enter()
		.append("circle")
		.attr(cx: () -> (Math.random() * (width - size)) + size/2)
		.attr(cy: () -> (Math.random() * (height - size)) + size/2)
		.attr(fill: "white")
		.attr(r: 0)

	interval = setInterval(() ->
		timeElapsed = index * speed
		timeText.text(() -> dateFormat(new Date(1,1,1,index/2,index%2 * 30)))
		if index >= (dataLength - 1) then index = 0

		if index >= startSunrise and index < startSunset and bg is "dark"
			body.transition().duration(speed * 24).style(background: "#454f5a")
			bg = "light"
		else if index >= startSunset and bg is "light"
			body.transition()
				.duration(speed * 24)
				.style(background: "#000")
			bg = "dark"

		circles.transition()
			.duration(speed)
			.ease("quad")
			.attr(r: (d) -> dayScale +d.entries[index].value)

		index++
	, speed)

queue()
	.defer(d3.csv, 'data/energy-consumption.csv')
	.await(graph)