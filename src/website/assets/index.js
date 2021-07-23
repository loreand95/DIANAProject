window.onload = (event) =>{
    draw();

    document.getElementById("exec").addEventListener("click", query);
    document.getElementById('form').addEventListener('submit', query);

    // Disable submit if query is empty
    document.getElementById("query").addEventListener('input',e => {
        let value = document.getElementById("query").value;
        document.getElementById("exec").disabled = !value
    })
}

var viz;

function draw() {
    var config = {
        container_id: "viz",
        server_url: "bolt://51.145.134.135:7687",
        server_user: "DIANAProject",
        server_password: "toga-adrian-circus-raymond-salami-1610",
        labels: {
            //"Character": "name",
            "Character": {
                "caption": "name",
                "size": "pagerank",
                "community": "community"
            }
        },
        relationships: {
            "INTERACTS": {
                "thickness": "weight",
                "caption": false
            }
        },
        initial_cypher: "MATCH (n) RETURN n LIMIT 25"
    };

    viz = new NeoVis.default(config);
    viz.render();
}

function query(){
    let query = document.getElementById('query').value
    viz.renderWithCypher(query)
}
