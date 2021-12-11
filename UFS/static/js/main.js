function creater() {
    swal(
        'Овчинников Алексей\ninst: allelleo',
        'создатель сайта',
        'success'
    )
}

function logINconsole(h1, h2) {
    console.log(h1 + " / " + h2)
}

function createArtcleSumbolsName() {
    var input = document.getElementById("createArtcleSumbolsName");
    var LimitSumbols = 150;

    input.oninput = function() {
        logINconsole(input.value.length, LimitSumbols);
        if (input.value.length < LimitSumbols) {
            document.getElementById('result').innerHTML = input.value.length + " / " + LimitSumbols;
            document.getElementById('result').style.color = "black"
        } else {
            document.getElementById('result').innerHTML = input.value.length + " / " + LimitSumbols;
            document.getElementById('result').style.color = "red"
        }
    };

}