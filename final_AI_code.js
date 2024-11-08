let rows = 25;
let cols = 25;
let windowSize = 800;
let cellSize = windowSize / Math.max(rows, cols);
let grid;
let agents = [];
let destinations = [];
let turn = 1;
let delay = 100;
let debug = false;
let images = {};
let path = [];

// p5.js setup function
function preload() {
  images.agent = loadImage('/uploads/naveen/agent.png');
  images.goal = loadImage('/uploads/naveen/goal.png');
  images.tree = loadImage('/uploads/naveen/tree_top.png');
}

function setup() {
  createCanvas(windowSize, windowSize);
  frameRate(10); 
  grid = new Grid(rows, cols);
  grid.populate();
  grid.computeAndAddSpotNeighbours();

  // Initialize agents with random positions and goals
  for (let i = 0; i < 4; i++) {
    let agent = new Agent(grid);
    console.log(`Agent create with i = ${agent.i} and j = ${agent.j}`)
    agents.push(agent);
    agent.startSpot.wall = false;
    agent.startSpot.agent = agent;
    agent.endSpot.wall = false;
    destinations.push(agent.endSpot);
  }
}

// p5.js draw loop
// Main loop
function draw() {
  background(255);
  
  // Each agent takes turns moving
  switch (turn % 4) {
    case 1: 
        moveAgent(agents[0], agents[0].startSpot, agents[0].endSpot); 
        break;
    case 2: moveAgent(agents[1], agents[1].startSpot, agents[1].endSpot); 
        break;
    case 3: moveAgent(agents[2], agents[2].startSpot, agents[2].endSpot); 
        break;
    case 0: moveAgent(agents[3], agents[3].startSpot, agents[3].endSpot); 
        break;
  }

  grid.show();
  turn++;
}

// Function to move each agent towards its goal
function moveAgent(agent, start, end) {
  if (agent.i !== end.i || agent.j !== end.j) {
    path = agent.getPath(start, end);
    grid.clear();
    if (path.length > 1) {
      start = path.shift();
    start = path.shift();
      agent.moveOneStep(start);
    
     
    }
  }
}

// Spot class
class Spot {
  constructor(i, j) {
    this.i = i;
    this.j = j;
    this.f = 0;
    this.g = 0;
    this.h = 0;
    this.neighbours = [];
    this.previous = null;
    this.wall = random() < 0.25;
    this.agent = false;
  }

  draw() {
    let x = this.i * cellSize;
    let y = this.j * cellSize;
    noStroke();

    if (this.agent) {
      image(images.agent, this.agent.i * cellSize, this.agent.j * cellSize, cellSize, cellSize);
      //console.log(this.agent.i,this.agent.j);
    } else if (this.wall) {
      image(images.tree, x, y, cellSize, cellSize);
    } else if (destinations.includes(this)) {
      image(images.goal, x, y, cellSize, cellSize);
    } else if (path.includes(this)) {
      fill(100, 200, 255);
      rect(x, y, cellSize, cellSize);
    } else {
      fill(144, 238, 144);
      rect(x, y, cellSize, cellSize);
    }
  }
}

// Grid class
class Grid {
  constructor(rows, cols) {
    this.rows = rows;
    this.cols = cols;
    this.spots = new Array(rows).fill().map(() => new Array(cols));
  }

  populate() {
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        this.spots[i][j] = new Spot(i, j);
      }
    }
  }

  computeAndAddSpotNeighbours() {
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        let spot = this.spots[i][j];
        if (i > 0) spot.neighbours.push(this.spots[i - 1][j]);
        if (i < cols - 1) spot.neighbours.push(this.spots[i + 1][j]);
        if (j > 0) spot.neighbours.push(this.spots[i][j - 1]);
        if (j < rows - 1) spot.neighbours.push(this.spots[i][j + 1]);
        console.log(i)
      }
    }
  }

  show() {
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        this.spots[i][j].draw();
      }
    }
  }

  clear() {
    for (let row of this.spots) {
      for (let spot of row) {
        spot.f = spot.g = spot.h = 0;
        spot.previous = null;
      }
    }
  }

  static heuristic(spot1, spot2) {
    return abs(spot1.i - spot2.i) + abs(spot1.j - spot2.j);
  }
}

// Agent class
class Agent {
  constructor(grid) {
    this.grid = grid;
    this.i = floor(random(rows));
    this.j = floor(random(cols));
    this.startSpot = grid.spots[this.i][this.j];
    this.endSpot = grid.spots[floor(random(rows))][floor(random(cols))];
    // this.path = [];
    this.openSet = [];
    this.closedSet = [];
  }

  getPath(start, destination) {
    if (debug) console.log("Get path was called..");
    this.path = [];
    this.openSet = [start];
    this.closedSet = [];

    start.g = 0;
    start.h = Grid.heuristic(start, destination);
    start.f = start.g + start.h;

    while (this.openSet.length > 0) {
      let current = this.openSet.reduce((a, b) => (a.f < b.f ? a : b));
      if (current === destination) {
        this.path = [];
        while (current) {
          this.path.push(current);
          current = current.previous;
        }
        this.path.reverse();
        return this.path;
      }

      this.openSet = this.openSet.filter(s => s !== current);
      this.closedSet.push(current);

      for (let neighbor of current.neighbours) {
        if (!this.closedSet.includes(neighbor) && !neighbor.wall && !neighbor.agent) {
          let tempG = current.g + 1;

          if (!this.openSet.includes(neighbor) || tempG < neighbor.g) {
            neighbor.previous = current;
            neighbor.g = tempG;
            neighbor.h = Grid.heuristic(neighbor, destination);
            neighbor.f = neighbor.g + neighbor.h;
            if (!this.openSet.includes(neighbor)) {
              this.openSet.push(neighbor);
            }
          }
        }
      }
    }

    if (debug) console.log("No Path was found...");
    return [];
  }

  moveOneStep(step) {
    let { i, j } = step;
    console.log(step);
    this.grid.spots[this.i][this.j].agent = null;
    this.i = i;
    this.j = j;
    this.startSpot = grid.spots[this.i][this.j]
    this.grid.spots[i][j].agent = this;
  }
}
