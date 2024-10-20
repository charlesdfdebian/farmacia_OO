// Função para formatar o número de telefone ao digitar
document.getElementById('telefone').addEventListener('input', function (e) {
    var x = e.target.value.replace(/\D/g, ''); // Remove qualquer caractere que não seja número
    if (x.length > 0) {
        x = '(' + x.substring(0, 2) + ') ' + (x.length > 5 ? x.substring(2, 6) + '-' + x.substring(6, 10) : x.substring(2, 6));
    }
    e.target.value = x;
});
