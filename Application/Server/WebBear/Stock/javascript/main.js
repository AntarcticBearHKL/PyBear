window.onload = function(){
    window.onresize()
    var vue = new Vue({
        el: '#context',
        data: {
            input: '',
            drawer: true,
        },
        methods: {
            pofu: function(){
                this.$http.post('/Welcome/api', {a:'haha'}).then(function(res){
                    alert('a')    
                },function(){
                    console.log('请求失败处理');
                });
            }
        }
    })

}

window.onresize = function(){
    wwidth = document.getElementById('Background').clientWidth
    wheight = document.getElementById('Background').clientHeight

    document.getElementById('sidebar').style.height = wheight - 50 + 'px'

    document.getElementById('panel').style.height = wheight - 50 + 'px'
    document.getElementById('panel').style.width = wwidth - 330 + 'px'
    document.getElementById('panel').style.top = '20px'
    document.getElementById('panel').style.left = '300px'
}