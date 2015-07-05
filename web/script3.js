// Generated by CoffeeScript 1.9.3
(function() {
  var graph;

  graph = function(e, data) {
    var baseSpeed, bg, body, circles, connection, contain, dataByDate, dataByHousehold, dataLength, dateFormat, day, dayData, dayIndex, dayMax, dayMin, dayScale, elapsed, height, index, interval, multiplier, numHouseholds, size, speed, startSunrise, startSunset, svg, t1, t2, timeLine, timeScale, timeText, width, wsuri;
    contain = d3.select(".content");
    dataByHousehold = d3.nest().key(function(d) {
      return d.respondent;
    }).entries(data);
    dataByDate = d3.nest().key(function(d) {
      return d["OUTPUT_DATE"];
    }).entries(data);
    console.log(dataByDate);
    dayIndex = 119;
    dayData = dataByDate[dayIndex].values.filter(function(d) {
      return d["TYPE"] === "general";
    });
    dayData = (function() {
      var i, len, results;
      results = [];
      for (i = 0, len = dayData.length; i < len; i++) {
        day = dayData[i];
        results.push({
          id: day["respondent"],
          data: day["OUTPUT_DATE"],
          entries: d3.entries(day).slice(3)
        });
      }
      return results;
    })();
    dayMin = d3.min(dayData, function(d) {
      return d3.min(d.entries, function(e) {
        return +e.value;
      });
    });
    dayMax = d3.max(dayData, function(d) {
      return d3.max(d.entries, function(e) {
        return +e.value;
      });
    });
    numHouseholds = dataByHousehold.length;
    dataLength = dayData[0].entries.length;
    console.log(dataLength);
    size = 100;
    baseSpeed = 1000;
    multiplier = 1;
    speed = baseSpeed * multiplier;
    index = 0;
    elapsed = 0;
    width = 1000;
    height = 800;
    startSunrise = 0;
    startSunset = 12 * 2;
    dateFormat = d3.time.format("%I:%M%p");
    dayScale = d3.scale.pow().domain([dayMin, dayMax]).range([0, size / 2]);
    timeScale = d3.time.scale().range([1, 100]);
    body = d3.select("body");
    svg = contain.append("svg").attr({
      width: width
    }).attr({
      height: height
    });
    timeText = contain.append("div").attr({
      "class": "time"
    });
    timeLine = contain.append("div").attr({
      "class": "timeline"
    }).append("svg").attr({
      width: "100%"
    }).attr({
      height: 40
    });
    body.style({
      background: "#000"
    });
    body.transition().duration(speed * startSunset).style({
      background: "#454f5a"
    });
    bg = "light";
    circles = svg.selectAll("circle").data(dayData).enter().append("circle").attr({
      cx: function() {
        return (Math.random() * (width - size)) + size / 2;
      }
    }).attr({
      cy: function() {
        return (Math.random() * (height - size)) + size / 2;
      }
    }).attr({
      fill: "white"
    }).attr({
      r: 0
    });
    interval = setInterval(function() {
      var timeElapsed;
      timeElapsed = index * speed;
      timeText.text(function() {
        return dateFormat(new Date(1, 1, 1, index / 2, index % 2 * 30));
      });
      if (index >= (dataLength - 1)) {
        index = 0;
      }
      if (index >= startSunrise && index < startSunset && bg === "dark") {
        body.transition().duration(speed * 24).style({
          background: "#454f5a"
        });
        bg = "light";
      } else if (index >= startSunset && bg === "light") {
        body.transition().duration(speed * 24).style({
          background: "#000"
        });
        bg = "dark";
      }
      circles.transition().duration(speed).ease("quad").attr({
        r: function(d) {
          return dayScale(+d.entries[index].value);
        }
      });
      return index++;
    }, speed);
    wsuri = "ws://127.0.0.1:8080/ws";
    connection = new autobahn.Connection({
      url: wsuri,
      realm: "realm1"
    });
    t1 = 0;
    t2 = 0;
    connection.onopen = function(session, details) {
      var mul2, on_counter;
      console.log("Connected");
      on_counter = function(args) {
        return console.log(args);
      };
      session.subscribe('com.example.counter', on_counter).then(function(sub) {
        return console.log('subscribed to topic');
      }, function(err) {
        return console.log('failed to subscribe to topic', err);
      });
      mul2 = function(args) {
        var x, y;
        x = args[0];
        y = args[1];
        console.log("mul2() called with " + x + " and " + y);
        return x * y;
      };
      return session.register('com.example.mul2', mul2).then(function(reg) {
        return console.log('procedure registered');
      }, function(err) {
        return console.log('failed to register procedure', err);
      });
    };
    connection.onclose = function(reason, details) {
      console.log("Connection lost: " + reason);
      if (t1) {
        clearInterval(t1);
        t1 = null;
      }
      if (t2) {
        clearInterval(t2);
        return t2 = null;
      }
    };
    return connection.open();
  };

  queue().defer(d3.csv, 'data/energy-consumption.csv').await(graph);

}).call(this);
