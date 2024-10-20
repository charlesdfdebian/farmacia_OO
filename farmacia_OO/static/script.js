document.getElementById('telefone').addEventListener('input', function (e) {
    var x = e.target.value.replace(/\D/g, ''); // Remove qualquer caractere que não seja número
    
    if (x.length > 0) {
        if (x.length <= 10) {
            // Formato para números fixos: (XX) XXXX-XXXX
            x = '(' + x.substring(0, 2) + ') ' + x.substring(2, 6) + '-' + x.substring(6, 10);
        } else {
            // Formato para números móveis: (XX) XXXXX-XXXX
            x = '(' + x.substring(0, 2) + ') ' + x.substring(2, 7) + '-' + x.substring(7, 11);
        }
    }
    e.target.value = x;
});
