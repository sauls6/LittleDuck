program ejemplo;
var x, y : int;
    resultado : float;

void calcular(num : int, factor : float) [
    var temp : float;
    {
    temp = num * factor;
    print("Resultado:", temp);
    }
];

main {
    x = 10;
    y = 5;
    resultado = x + y * 2.5;
    calcular(x, resultado);
    
    if (x > y) {
        print("x es mayor que y");
    } else {
        print("y es mayor o igual a x");
    };
    
    while (y > 0) do {
        print("Contador:", y);
        y = y - 1;
    };
}
end
